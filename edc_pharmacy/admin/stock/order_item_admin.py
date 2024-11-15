from decimal import Decimal

from django.contrib import admin
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html
from django_audit_fields.admin import audit_fieldset_tuple
from edc_constants.constants import COMPLETE

from ...admin_site import edc_pharmacy_admin
from ...forms import OrderItemForm
from ...models import Order, OrderItem, Receive, Stock
from ...utils import format_qty
from ..list_filters import ProductAssignmentListFilter
from ..model_admin_mixin import ModelAdminMixin
from ..remove_fields_for_blinded_users import remove_fields_for_blinded_users


@admin.register(OrderItem, site=edc_pharmacy_admin)
class OrderItemAdmin(ModelAdminMixin, admin.ModelAdmin):
    change_list_title = "Pharmacy: Ordered items"
    show_object_tools = False
    show_cancel = True
    list_per_page = 20

    form = OrderItemForm
    ordering = ("-order_item_identifier",)
    autocomplete_fields = ["product", "container"]

    fieldsets = (
        (
            None,
            {"fields": (["order", "product", "container"])},
        ),
        (
            "Quantity",
            {"fields": (["qty", "unit_qty", "unit_qty_received"])},
        ),
        ("Status", {"fields": (["status"])}),
        audit_fieldset_tuple,
    )

    list_display = (
        "identifier",
        "product__name",
        "assignment",
        "container",
        "formatted_qty",
        "formatted_unit_qty",
        "status",
        "order_changelist",
        "receive_url",
        "stock_changelist",
        "created",
        "modified",
    )
    list_filter = (
        "status",
        ProductAssignmentListFilter,
    )
    radio_fields = {"status": admin.VERTICAL}
    search_fields = (
        "id",
        "order__id",
        "order__order_identifier",
    )
    readonly_fields = (
        "unit_qty",
        "unit_qty_received",
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

    @admin.display(description="ORDER ITEM #", ordering="-order_item_identifier")
    def identifier(self, obj):
        return obj.order_item_identifier

    @admin.display(description="Assignment", ordering="product__assignment__name")
    def assignment(self, obj):
        return obj.product.assignment

    @admin.display(description="QTY", ordering="qty")
    def formatted_qty(self, obj):
        return format_qty(obj.qty, obj.container)

    @admin.display(description="Units", ordering="qty")
    def formatted_unit_qty(self, obj):
        return format_qty(obj.unit_qty, obj.container)

    @admin.display(description="Product", ordering="product__name")
    def product_name(self, obj):
        return obj.product.formulation.get_description_with_assignment(obj.product.assignment)

    @admin.display(description="Container", ordering="container__name")
    def container_name(self, obj):
        return obj.container.name

    @admin.display(description="Order #", ordering="-order__order_datetime")
    def order_changelist(self, obj):
        url = reverse("edc_pharmacy_admin:edc_pharmacy_order_changelist")
        url = f"{url}?q={obj.order.order_identifier}"
        context = dict(url=url, label=obj.order.order_identifier, title="Back to order")
        return render_to_string("edc_pharmacy/stock/items_as_link.html", context=context)

    @admin.display(description="to receive", ordering="unit_qty_received")
    def received_items_changelist(self, obj):
        if (obj.unit_qty_received or Decimal(0)) > Decimal(0):
            url = reverse("edc_pharmacy_admin:edc_pharmacy_receiveitem_changelist")
            url = f"{url}?q={str(obj.id)}"
            label = format_qty(obj.unit_qty - obj.unit_qty_received, obj.container)
            context = dict(
                url=url,
                label=label,
                title="Go to received item(s) for this ordered item",
            )
            return render_to_string("edc_pharmacy/stock/items_as_link.html", context=context)
        return None

    @admin.display(description="Stock")
    def stock_changelist(self, obj):
        if Stock.objects.filter(receive_item__receive__order=obj.order).exists():
            url = reverse("edc_pharmacy_admin:edc_pharmacy_stock_changelist")
            url = f"{url}?q={obj.order.id}"
            context = dict(url=url, label="Stock", title="Go to stock")
            return render_to_string("edc_pharmacy/stock/items_as_link.html", context=context)
        return None

    @admin.display(description="Receive #")
    def receive_url(self, obj):
        (
            str_start_receiving_button,
            str_receive_this_item_button,
            str_received_items_link,
            str_receive_changelist_link,
        ) = (
            "",
            "",
            "",
            "",
        )
        try:
            rcv_obj = Receive.objects.get(order=obj.order)
        except Receive.DoesNotExist:
            rcv_obj = None
        if not rcv_obj:
            url = reverse("edc_pharmacy_admin:edc_pharmacy_receive_add")
            next_url = "edc_pharmacy_admin:edc_pharmacy_orderitem_changelist"
            url = f"{url}?next={next_url}&q={str(obj.order.id)}&order={str(obj.order.id)}"
            context = dict(
                url=url, label="Start Receiving", title="Receive against this order item"
            )
            str_start_receiving_button = render_to_string(
                "edc_pharmacy/stock/items_as_button.html", context=context
            )
        else:
            url = reverse("edc_pharmacy_admin:edc_pharmacy_receive_changelist")
            url = f"{url}?q={str(rcv_obj.receive_identifier)}"
            context = dict(url=url, label=rcv_obj.receive_identifier, title="Receive")
            str_receive_changelist_link = render_to_string(
                "edc_pharmacy/stock/items_as_link.html", context=context
            )
        if rcv_obj:
            if obj.status != COMPLETE:
                url = reverse("edc_pharmacy_admin:edc_pharmacy_receiveitem_add")
                next_url = "edc_pharmacy_admin:edc_pharmacy_orderitem_changelist"
                url = (
                    f"{url}?next={next_url}&order_item={str(obj.id)}&q={str(obj.order.id)}"
                    f"&receive={str(rcv_obj.id)}&container={str(obj.container.id)}"
                )
                context = dict(
                    url=url, label="Receive this item", title="Receive against this order item"
                )
                str_receive_this_item_button = render_to_string(
                    "edc_pharmacy/stock/items_as_button.html", context=context
                )
            else:
                url = reverse("edc_pharmacy_admin:edc_pharmacy_receiveitem_changelist")
                url = f"{url}?q={str(obj.order.order_identifier)}"
                context = dict(url=url, label="Received items", title="Received items")
                str_received_items_link = render_to_string(
                    "edc_pharmacy/stock/items_as_link.html", context=context
                )
        renders = [
            str_start_receiving_button,
            str_receive_changelist_link,
            str_receive_this_item_button,
            str_received_items_link,
        ]
        renders = [r for r in renders if r]
        return format_html("<BR>".join(renders))

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("order",)
        return self.readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "order":
            if request.GET.get("order"):
                kwargs["queryset"] = Order.objects.filter(
                    id__exact=request.GET.get("order", 0)
                )
            else:
                kwargs["queryset"] = Order.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
