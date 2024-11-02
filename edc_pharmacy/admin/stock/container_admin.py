from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ...admin_site import edc_pharmacy_admin
from ...forms import ContainerForm
from ...models import Container
from ..model_admin_mixin import ModelAdminMixin


@admin.register(Container, site=edc_pharmacy_admin)
class ContainerAdmin(ModelAdminMixin, admin.ModelAdmin):
    show_object_tools = True

    form = ContainerForm

    fieldsets = (
        (
            None,
            {"fields": (["name", "container_type", "units", "qty", "may_receive_as"])},
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "name",
        "container_type",
        "units",
        "qty",
        "may_receive_as",
        "created",
        "modified",
    )
    list_filter = ("container_type", "units", "may_receive_as", "created")
    radio_fields = {"container_type": admin.VERTICAL, "units": admin.VERTICAL}
    search_fields = ("name",)
    ordering = ("name",)
