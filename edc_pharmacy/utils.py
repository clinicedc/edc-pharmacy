from __future__ import annotations

import base64
import string
from binascii import Error
from decimal import Decimal
from typing import TYPE_CHECKING

from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from edc_registration.models import RegisteredSubject
from edc_visit_tracking.utils import get_previous_related_visit

from .exceptions import (
    ChecksumError,
    InsufficientStockError,
    ProcessStockRequestError,
    RepackError,
    StockError,
)

if TYPE_CHECKING:
    from .models import Container, Location, RepackRequest, Stock, StockRequest


def format_qty(qty: Decimal, container: Container):
    if container.qty_decimal_places == 0:
        return str(int(qty))
    elif container.qty_decimal_places == 1:
        return "{:0.1f}".format(qty)
    return "{:0.2f}".format(qty)


def get_rxrefill_model_cls():
    return django_apps.get_model("edc_pharmacy.rxrefill")


def get_rx_model_cls():
    return django_apps.get_model("edc_pharmacy.rx")


def update_previous_refill_end_datetime(instance):
    """Update refill_end_datetime from previous visit relative to the
    refill_start_datetime of this visit.
    """
    if previous_visit := get_previous_related_visit(
        instance.related_visit, include_interim=True
    ):
        opts = {instance.__class__.related_visit_model_attr(): previous_visit}
        try:
            obj = instance.__class__.objects.get(**opts)
        except ObjectDoesNotExist:
            pass
        else:
            obj.refill_end_datetime = instance.refill_start_datetime - relativedelta(seconds=1)
            obj.save_base(update_fields=["refill_end_datetime"])


# def repackage_stock_from_packaging_request(
#     stock: Stock, container: Container, repackaging_request
# ):
#     repackage_stock(
#         stock,
#         container,
#         stock.location,
#         stock.location,
#         repackaging_request=repackaging_request,
#     )
#
#
# def repackage_stock_from_request_item():
#     repackage_stock()
#
def get_and_check_stock(stock_identifier):
    stock = Stock.objects.get(stock_identifier=stock_identifier)
    if not stock.confirmed:
        raise StockError(f"Stock item is not confirmed. Unable to process. Got {stock}.")
    if stock.unit_qty_in - stock.unit_qty_out == Decimal(0):
        raise InsufficientStockError(
            f"Not in stock. Cannot repack. Got stock {stock.stock_identifier}."
        )
    if stock.unit_qty_in - stock.unit_qty_out < 0:
        raise StockError(
            "Stock `unit qty` is wrong. Unit qty IN cannot be less than unit qty OUT. "
            f"Got stock {stock.stock_identifier}."
        )
    return stock


def process_repack_request(
    repack_request: RepackRequest | None = None,
) -> RepackRequest:
    """Take from stock and fill container as new stock item.

    Do not change location here.
    """
    if repack_request.from_stock and not repack_request.processed:
        if not repack_request.from_stock.confirmed:
            raise RepackError("Stock not confirmed")
        for index in range(0, int(repack_request.qty)):
            repack_request.from_stock.__class__.objects.create(
                receive_item=None,
                qty_in=1,
                from_stock=repack_request.from_stock,
                container=repack_request.container,
                location=repack_request.from_stock.location,
                repack_request=repack_request,
                confirmed=False,
                lot=repack_request.from_stock.lot,
            )
        repack_request.processed = True
        repack_request.save()
    return repack_request


def process_stock_request(
    stock_request: StockRequest, source_location: Location, source_container: Container
):

    # TODO: look at available local stock first before checking central stock

    qs = (
        RegisteredSubject.objects.values("randomization_list_model")
        .filter(randomization_list_model__isnull=False)
        .annotate(model_name=Count("randomization_list_model"))
    )
    if qs.count() > 1:
        raise ProcessStockRequestError("More than one randomization_list_model found.")
    model_cls = django_apps.get_model(qs.filter()[0]["randomization_list_model"])
    for stock_request_item in django_apps.get_model(
        "edc_pharmacy.stockrequestitem"
    ).objects.filter(stock_request=stock_request):

        rando = model_cls.objects.get(subject_identifier=stock_request_item.subject_identifier)
        stock_request_item.sid = rando.sid
        stock_request_item.site = rando.allocated_site
        stock_request_item.gender = RegisteredSubject.objects.get(
            subject_identifier=stock_request_item.subject_identifier
        ).gender
        stock_request_item.save()

        assignment = django_apps.get_model("edc_pharmacy.assignment").objects.get(
            name=rando.assignment
        )

        stock = django_apps.get_model("edc_pharmacy.stock").objects.in_stock(
            unit_qty=stock_request_item.stock_request.container.qty,
            container=source_container,
            assignment=assignment,
            location=source_location,
        )
        if stock:
            process_repack_request(
                stock,
                stock_request_item.stock_request.container,
                stock_request_item=stock_request_item,
            )


def generate_code_with_checksum_from_id(id_number: int) -> str:
    bytes_id = id_number.to_bytes((id_number.bit_length() + 7) // 8, "big")
    code = base64.b32encode(bytes_id).decode("utf-8")
    code = code.rstrip("=")
    checksum = sum(ord(c) * (i + 1) for i, c in enumerate(code)) % 36
    checksum_char = (
        string.digits[checksum] if checksum < 10 else string.ascii_uppercase[checksum - 10]
    )
    return code + checksum_char


def decode_code_with_checksum(code: str) -> int:
    if code != add_checksum(code[:-1]):
        raise ChecksumError(f"Invalid checksum for code. Got {code}")
    padding_length = (8 - (len(code[:-1]) % 8)) % 8
    padded_code = code[:-1] + ("=" * padding_length)
    try:
        decoded_bytes = base64.b32decode(padded_code)
    except Error as e:
        raise ValueError(f"Failed to decode string: {str(e)}")
    return int.from_bytes(decoded_bytes, "big")


def add_checksum(code):
    checksum = sum(ord(c) * (i + 1) for i, c in enumerate(code)) % 36
    checksum_char = (
        string.digits[checksum] if checksum < 10 else string.ascii_uppercase[checksum - 10]
    )
    return code + checksum_char
