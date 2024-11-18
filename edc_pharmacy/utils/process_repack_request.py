from __future__ import annotations

from uuid import UUID

from django.apps import apps as django_apps

from ..exceptions import InsufficientStockError, RepackError


def process_repack_request(repack_request_id: UUID | None = None) -> None:
    """Take from stock and fill container as new stock item.

    Do not change location here.
    """
    repack_request_model_cls = django_apps.get_model("edc_pharmacy.repackrequest")
    stock_model_cls = django_apps.get_model("edc_pharmacy.stock")
    repack_request = repack_request_model_cls.objects.get(id=repack_request_id)
    repack_request.task_id = None
    repack_request.processed_qty = repack_request.processed_qty = (
        stock_model_cls.objects.filter(repack_request=repack_request).count()
    )
    repack_request.requested_qty = (
        repack_request.processed_qty
        if not repack_request.requested_qty
        else repack_request.requested_qty
    )
    number_to_process = repack_request.requested_qty - repack_request.processed_qty
    if not repack_request.from_stock.confirmed:
        raise RepackError("Source stock item not confirmed")
    else:
        stock_model_cls = repack_request.from_stock.__class__
        for index in range(0, int(number_to_process)):
            try:
                stock_model_cls.objects.create(
                    receive_item=None,
                    qty_in=1,
                    qty_out=0,
                    qty=1,
                    from_stock=repack_request.from_stock,
                    container=repack_request.container,
                    location=repack_request.from_stock.location,
                    repack_request=repack_request,
                    confirmed=False,
                    lot=repack_request.from_stock.lot,
                )
            except InsufficientStockError:
                break
    repack_request.processed_qty = stock_model_cls.objects.filter(
        repack_request=repack_request
    ).count()
    repack_request.save(update_fields=["requested_qty", "processed_qty", "task_id"])
