from django.contrib import admin
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html
from django_audit_fields.admin import audit_fieldset_tuple

from ...admin_site import edc_pharmacy_admin
from ...exceptions import AllocationError, AssignmentError
from ...forms import StockForm
from ...models import RepackRequest, Stock
from ...utils import format_qty
from ..actions import (
    go_to_add_repack_request_action,
    print_labels,
    transfer_stock_action,
)
from ..list_filters import (
    AllocationListFilter,
    HasOrderNumFilter,
    HasReceiveNumFilter,
    HasRepackNumFilter,
    ProductAssignmentListFilter,
)
from ..model_admin_mixin import ModelAdminMixin
from ..remove_fields_for_blinded_users import remove_fields_for_blinded_users


@admin.register(Stock, site=edc_pharmacy_admin)
class StockAdmin(ModelAdminMixin, admin.ModelAdmin):
    change_list_title = "Pharmacy: Stock"
    change_form_title = "Pharmacy: Stock"
    show_object_tools = False
    show_cancel = True
    list_per_page = 20

    show_form_tools = True
    show_history_label = True
    autocomplete_fields = ["container"]

    actions = [go_to_add_repack_request_action, print_labels, transfer_stock_action]

    form = StockForm

    ordering = ("stock_identifier",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "stock_identifier",
                    "code",
                    "confirmed",
                    "location",
                )
            },
        ),
        (
            "Product",
            {"fields": ("product", "container")},
        ),
        (
            "Lot",
            {"fields": ("lot",)},
        ),
        (
            "Quantity",
            {"fields": ("qty_in", "qty_out", "unit_qty_in", "unit_qty_out")},
        ),
        (
            "Receive / Repack",
            {
                "fields": (
                    "receive_item",
                    "repack_request",
                    "from_stock",
                    "confirmed_by",
                    "confirmed_datetime",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "formatted_code",
        "from_stock_changelist",
        "formatted_confirmed",
        "allocated",
        "formatted_at_location",
        "formulation",
        "verified_assignment",
        "qty",
        "container_str",
        "unit_qty",
        "order_changelist",
        "receive_item_changelist",
        "repack_request_changelist",
        "stock_request_changelist",
        "allocation_changelist",
        "stock_transfer_item_changelist",
        "created",
        "modified",
    )
    list_filter = (
        "confirmed",
        AllocationListFilter,
        "at_location",
        ProductAssignmentListFilter,
        "product__formulation__description",
        "product__assignment__name",
        "lot",
        "location__display_name",
        "container",
        "confirmed_by",
        "confirmed_datetime",
        HasOrderNumFilter,
        HasReceiveNumFilter,
        HasRepackNumFilter,
        "created",
        "modified",
    )
    search_fields = (
        "stock_identifier",
        "from_stock__stock_identifier",
        "code",
        "from_stock__code",
        "receive_item__id",
        "receive_item__receive__id",
        "receive_item__order_item__order__id",
        "repack_request__id",
        "allocation__registered_subject__subject_identifier",
        "allocation__stock_request_item__id",
        "allocation__stock_request_item__stock_request__id",
        "allocation__id",
        "stocktransferitem__stock_transfer__id",
    )
    readonly_fields = (
        "code",
        "confirmed",
        "confirmed_by",
        "confirmed_datetime",
        "container",
        "from_stock",
        "location",
        "repack_request",
        "lot",
        "product",
        "qty_in",
        "qty_out",
        "unit_qty_in",
        "unit_qty_out",
        "receive_item",
        "stock_identifier",
    )

    def get_list_display(self, request):
        fields = super().get_list_display(request)
        fields = remove_fields_for_blinded_users(request, fields)
        return fields

    def get_list_filter(self, request):
        fields = super().get_list_filter(request)
        fields = remove_fields_for_blinded_users(request, fields)
        return fields

    def get_search_fields(self, request):
        fields = super().get_search_fields(request)
        fields = remove_fields_for_blinded_users(request, fields)
        return fields

    @admin.display(description="Assignment", ordering="lot__assignment__name")
    def verified_assignment(self, obj):
        try:
            obj.verify_assignment_or_raise()
        except AssignmentError:
            return format_html('<div style="color:red;">ERROR!</div>')
        except AllocationError:
            return format_html('<div style="color:red;">Allocation<BR>ERROR!</div>')
        return obj.lot.assignment

    @admin.display(description="Lot #", ordering="lot__lot_no")
    def formatted_lot(self, obj):
        return obj.lot.lot_no

    @admin.display(description="Stock #", ordering="-stock_identifier")
    def formatted_code(self, obj):
        return obj.code

    @admin.display(description="QTY", ordering="qty")
    def qty(self, obj):
        return format_qty(obj.qty_in - obj.qty_out, obj.container)

    @admin.display(description="Units", ordering="qty")
    def unit_qty(self, obj):
        return format_qty(obj.unit_qty_in - obj.unit_qty_out, obj.container)

    @admin.display(description="STOCK #", ordering="-stock_identifier")
    def identifier(self, obj):
        return obj.stock_identifier.split("-")[0]

    @admin.display(description="C", ordering="confirmed", boolean=True)
    def formatted_confirmed(self, obj):
        return obj.confirmed

    @admin.display(description="T", ordering="at_location", boolean=True)
    def formatted_at_location(self, obj):
        return obj.at_location

    @admin.display(description="A", ordering="allocation", boolean=True)
    def allocated(self, obj):
        if obj.allocation:
            return True
        elif not obj.allocation and obj.from_stock:
            return False
        return None

    @admin.display(description="T", boolean=True)
    def in_transit(self, obj):
        if not obj.allocation:
            return None
        elif obj.allocation.stock_request_item.stock_request.location != obj.location:
            return False
        elif obj.allocation.stock_request_item.stock_request.location == obj.location:
            return True

    @admin.display(description="Container", ordering="container_name")
    def container_str(self, obj):
        return format_html("<BR>".join(str(obj.container).split(" ")))

    @admin.display(description="formulation", ordering="product__formulation__name")
    def formulation(self, obj):
        return obj.product.formulation

    @admin.display(description="assignment", ordering="product__assignment__name")
    def assignment(self, obj):
        if obj.product.assignment:
            return obj.product.assignment
        return None

    @admin.display(description="From stock #")
    def from_stock_changelist(self, obj):
        if obj.from_stock:
            url = reverse("edc_pharmacy_admin:edc_pharmacy_stock_changelist")
            url = f"{url}?q={obj.from_stock.code}"
            context = dict(
                url=url,
                label=obj.from_stock.code,
                title="Go to stock",
            )
            return render_to_string("edc_pharmacy/stock/items_as_link.html", context=context)
        return None

    @admin.display(description="Order #", ordering="-order__order_datetime")
    def order_changelist(self, obj):
        if obj.receive_item and obj.receive_item.order_item.order:
            url = reverse("edc_pharmacy_admin:edc_pharmacy_order_changelist")
            url = f"{url}?q={obj.receive_item.order_item.order.order_identifier}"
            context = dict(
                url=url,
                label=obj.receive_item.order_item.order.order_identifier,
                title="Go to order",
            )
            return render_to_string("edc_pharmacy/stock/items_as_link.html", context=context)
        return None

    @admin.display(
        description="Receive #", ordering="-receive_item__receive__receive_datetime"
    )
    def receive_item_changelist(self, obj):
        if obj.receive_item:
            url = reverse("edc_pharmacy_admin:edc_pharmacy_receive_changelist")
            url = f"{url}?q={obj.receive_item.receive.receive_identifier}"
            context = dict(
                url=url,
                label=obj.receive_item.receive.receive_identifier,
                title="Go to receiving",
            )
            return render_to_string("edc_pharmacy/stock/items_as_link.html", context=context)
        return None

    @admin.display(description="Repack #", ordering="-repack_request__repack_datetime")
    def repack_request_changelist(self, obj):
        context = {}
        url = reverse("edc_pharmacy_admin:edc_pharmacy_repackrequest_changelist")
        if obj.repack_request:
            url = f"{url}?q={obj.repack_request.id}"
            context = dict(
                url=url,
                label=obj.repack_request.repack_identifier,
                title="Go to repack request",
            )
        elif RepackRequest.objects.filter(from_stock=obj).exists():
            url = f"{url}?q={obj.code}"
            context = dict(
                url=url,
                label="Repacks",
                title="Go to repack requests for this stock item",
            )
        if context:
            return render_to_string(
                "edc_pharmacy/stock/items_as_link.html",
                context=context,
            )
        return None

    @admin.display(
        description="Allocation #",
        ordering="-allocation__registered_subject__subject_identifier",
    )
    def allocation_changelist(self, obj):
        if obj.allocation:
            url = reverse("edc_pharmacy_admin:edc_pharmacy_allocation_changelist")
            url = f"{url}?q={obj.allocation.id}"
            context = dict(
                url=url,
                label=obj.allocation.registered_subject.subject_identifier,
                title="Go to allocation",
            )
            return render_to_string("edc_pharmacy/stock/items_as_link.html", context=context)
        return None

    @admin.display(
        description="Transfer #",
        ordering="stock_transfer_item.to_location",
    )
    def stock_transfer_item_changelist(self, obj):
        if obj.stocktransferitem:
            url = reverse("edc_pharmacy_admin:edc_pharmacy_stocktransferitem_changelist")
            url = f"{url}?q={obj.code}"
            context = dict(
                url=url,
                label=obj.location,
                title="Go to stock transfer item",
            )
            return render_to_string("edc_pharmacy/stock/items_as_link.html", context=context)
        return None

    @admin.display(description="Request #")
    def stock_request_changelist(self, obj):
        if obj.allocation:
            url = reverse("edc_pharmacy_admin:edc_pharmacy_stockrequest_changelist")
            url = f"{url}?q={obj.allocation.stock_request_item.stock_request.id}"
            context = dict(
                url=url,
                label=obj.allocation.stock_request_item.stock_request.request_identifier,
                title="Go to stock request",
            )
            return render_to_string("edc_pharmacy/stock/items_as_link.html", context=context)
        return None
