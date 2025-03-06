from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.urls import reverse
from django_audit_fields import audit_fieldset_tuple
from edc_model_admin.history import SimpleHistoryAdmin
from edc_utils.date import to_local

from ...admin_site import edc_pharmacy_admin
from ...models import StockTransferItem
from ..model_admin_mixin import ModelAdminMixin


@admin.register(StockTransferItem, site=edc_pharmacy_admin)
class StockTransferItemAdmin(ModelAdminMixin, SimpleHistoryAdmin):
    change_list_title = "Pharmacy: Stock Transfer Item"
    change_form_title = "Pharmacy: Stock Transfer Items"
    history_list_display = ()
    show_object_tools = True
    show_cancel = True
    list_per_page = 20

    autocomplete_fields = ["stock"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "transfer_item_identifier",
                    "transfer_item_datetime",
                    "stock",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "identifier",
        "transfer_item_date",
        "stock_transfer_changelist",
        "stock_changelist",
        "stock__location",
        "stock_transfer_confirmation_item_changelist",
        "allocation_changelist",
    )

    list_filter = ("transfer_item_datetime",)

    search_fields = (
        "id",
        "transfer_item_identifier",
        "stock_transfer__id",
        "stock__code",
        "stock__allocation__registered_subject__subject_identifier",
    )

    readonly_fields = (
        "transfer_item_identifier",
        "transfer_item_datetime",
        "stock",
    )

    @admin.display(description="TRANSFER ITEM #", ordering="transfer_item_identifier")
    def identifier(self, obj):
        return obj.transfer_item_identifier

    @admin.display(description="Transfer date", ordering="transfer_item_datetime")
    def transfer_item_date(self, obj):
        return to_local(obj.transfer_item_datetime).date()

    @admin.display(description="Stock #", ordering="stock__code")
    def stock_changelist(self, obj):
        url = reverse("edc_pharmacy_admin:edc_pharmacy_stock_changelist")
        url = f"{url}?q={obj.stock.code}"
        context = dict(url=url, label=obj.stock.code, title="Go to stock")
        return render_to_string("edc_pharmacy/stock/items_as_link.html", context=context)

    @admin.display(
        description="Allocation",
        ordering="stock__allocation__registered_subject__subject_identifier",
    )
    def allocation_changelist(self, obj):
        subject_identifier = obj.stock.allocation.registered_subject.subject_identifier
        url = reverse("edc_pharmacy_admin:edc_pharmacy_allocation_changelist")
        url = f"{url}?q={subject_identifier}"
        context = dict(url=url, label=subject_identifier, title="Go to allocation")
        return render_to_string("edc_pharmacy/stock/items_as_link.html", context=context)

    @admin.display(description="Transfer #", ordering="stock_transfer__transfer_identifier")
    def stock_transfer_changelist(self, obj):
        url = reverse("edc_pharmacy_admin:edc_pharmacy_stocktransfer_changelist")
        url = f"{url}?q={obj.stock_transfer.id}"
        context = dict(
            url=url, label=obj.stock_transfer.transfer_identifier, title="Go to stock transfer"
        )
        return render_to_string("edc_pharmacy/stock/items_as_link.html", context=context)

    @admin.display(
        description="Site Confirmation #",
        ordering="stock__stocktransferconfirmationitem__transfer_confirmation_item_identifier",
    )
    def stock_transfer_confirmation_item_changelist(self, obj):
        try:
            transfer_confirmation_item = obj.stock.stocktransferconfirmationitem
        except ObjectDoesNotExist:
            pass
        else:
            url = reverse(
                "edc_pharmacy_admin:edc_pharmacy_stocktransferconfirmationitem_changelist"
            )
            url = f"{url}?q={transfer_confirmation_item.pk}"
            context = dict(
                url=url,
                label=transfer_confirmation_item.transfer_confirmation_item_identifier,
                title="Go to stock transfer confirmation item",
            )
            return render_to_string("edc_pharmacy/stock/items_as_link.html", context=context)
        return None
