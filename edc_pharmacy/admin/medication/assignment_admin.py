from typing import Tuple

from django import forms
from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ...admin_site import edc_pharmacy_admin
from ...models import Assignment
from ..model_admin_mixin import ModelAdminMixin


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = "__all__"


@admin.register(Assignment, site=edc_pharmacy_admin)
class AssignmentAdmin(ModelAdminMixin, admin.ModelAdmin):
    show_object_tools = True

    form = AssignmentForm

    fieldsets = (
        (
            None,
            {"fields": ["assignment", "display_label"]},
        ),
        audit_fieldset_tuple,
    )

    list_display: Tuple[str, ...] = (
        "assignment",
        "display_label",
        "created",
        "modified",
    )

    search_fields: Tuple[str, ...] = ("assignment", "display_label")
