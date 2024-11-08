from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ...admin_site import edc_pharmacy_admin
from ...forms import ContainerForm
from ...models import Container
from ...utils import format_qty
from ..model_admin_mixin import ModelAdminMixin


@admin.register(Container, site=edc_pharmacy_admin)
class ContainerAdmin(ModelAdminMixin, admin.ModelAdmin):
    change_list_title = "Pharmacy: Containers"
    show_object_tools = True

    form = ContainerForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    [
                        "name",
                        "container_type",
                        "units",
                        "qty",
                        "qty_decimal_places",
                        "may_order_as",
                        "may_receive_as",
                        "may_repack_as",
                        "may_request_as",
                        "may_dispense_as",
                    ]
                )
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "name",
        "container_type",
        "formatted_units",
        "decimal_places",
        "may_order",
        "may_receive",
        "may_repack",
        "may_request",
        "may_dispense",
        "created",
        "modified",
    )
    list_filter = (
        "container_type",
        "units",
        "may_order_as",
        "may_receive_as",
        "may_repack_as",
        "may_request_as",
        "may_dispense_as",
        "created",
    )
    radio_fields = {"container_type": admin.VERTICAL, "units": admin.VERTICAL}
    search_fields = ("name",)
    ordering = ("name",)

    @admin.display(description="Units", ordering="units")
    def formatted_units(self, obj):
        if obj.qty > 1:
            return f"{format_qty(obj.qty, obj)} {obj.units.plural_name}"
        return f"{format_qty(obj.qty, obj)} {obj.units.display_name}"

    @admin.display(description="Places", ordering="qty_decimal_places")
    def decimal_places(self, obj):
        return obj.qty_decimal_places

    @admin.display(description="order", ordering="may_order_as", boolean=True)
    def may_order(self, obj):
        return obj.may_order_as

    @admin.display(description="receive", ordering="may_receive_as", boolean=True)
    def may_receive(self, obj):
        return obj.may_receive_as

    @admin.display(description="Repack", ordering="may_repack_as", boolean=True)
    def may_repack(self, obj):
        return obj.may_repack_as

    @admin.display(description="request", ordering="may_request_as", boolean=True)
    def may_request(self, obj):
        return obj.may_request_as

    @admin.display(description="dispense", ordering="may_dispense_as", boolean=True)
    def may_dispense(self, obj):
        return obj.may_dispense_as
