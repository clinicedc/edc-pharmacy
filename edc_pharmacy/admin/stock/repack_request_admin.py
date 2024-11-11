from django.contrib import admin
from django.template.loader import render_to_string
from django.urls import reverse
from django_audit_fields import audit_fieldset_tuple
from edc_utils.date import to_local

from ...admin_site import edc_pharmacy_admin
from ...forms import RepackRequestForm
from ...models import RepackRequest
from ...utils import format_qty
from ..actions import confirm_repacked_stock_action, process_repack_request_action
from ..model_admin_mixin import ModelAdminMixin


@admin.register(RepackRequest, site=edc_pharmacy_admin)
class RequestRepackAdmin(ModelAdminMixin, admin.ModelAdmin):
    change_list_title = "Pharmacy: Repackage request"
    change_form_title = "Pharmacy: Repack"
    show_object_tools = True
    show_cancel = True
    autocomplete_fields = ["container"]
    form = RepackRequestForm
    actions = [process_repack_request_action, confirm_repacked_stock_action]

    fieldsets = (
        (
            "Section A: Repack",
            {
                "fields": (
                    "repack_identifier",
                    "repack_datetime",
                    "from_stock",
                    "container",
                    "qty",
                    "label_configuration",
                )
            },
        ),
        (
            "Section B: Confirm stock after labelling",
            {
                "description": (
                    "Fill in AFTER repack is complete. Save the form, print labels, "
                    "label stock, then return here to confirm stock"
                ),
                "fields": (
                    "stock_count",
                    "stock_identifiers",
                    "confirmed_stock_identifiers",
                    "unconfirmed_stock_identifiers",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "identifier",
        "repack_date",
        "from_stock_changelist",
        "formatted_qty",
        "container",
        "from_stock__product__name",
        "processed",
        "stock_changelist",
    )

    search_fields = ("id", "container__name")
    readonly_fields = ("confirmed_stock_identifiers", "unconfirmed_stock_identifiers")

    @admin.display(description="Repack date", ordering="repack_datetime")
    def repack_date(self, obj):
        return to_local(obj.repack_datetime).date()

    @admin.display(description="Stock")
    def stock_changelist(self, obj):
        url = reverse("edc_pharmacy_admin:edc_pharmacy_stock_changelist")
        url = f"{url}?q={obj.id}"
        context = dict(url=url, label="Stock", title="Go to stock")
        return render_to_string("edc_pharmacy/stock/items_as_link.html", context=context)

    @admin.display(description="From stock")
    def from_stock_changelist(self, obj):
        url = reverse("edc_pharmacy_admin:edc_pharmacy_stock_changelist")
        url = f"{url}?q={obj.from_stock.id}"
        context = dict(url=url, label=obj.from_stock.stock_identifier, title="Go to stock")
        return render_to_string("edc_pharmacy/stock/items_as_link.html", context=context)

    @admin.display(description="REPACK #", ordering="-repack_identifier")
    def identifier(self, obj):
        return obj.repack_identifier

    @admin.display(description="QTY", ordering="qty")
    def formatted_qty(self, obj):
        return format_qty(obj.qty, obj.container)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "from_stock" and request.GET.get("from_stock"):
            kwargs["queryset"] = db_field.related_model.objects.filter(
                pk=request.GET.get("from_stock", 0)
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
