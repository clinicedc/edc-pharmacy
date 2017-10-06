from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_base.modeladmin_mixins import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminReadOnlyMixin, ModelAdminInstitutionMixin)
from edc_pharma.models import DispenseAppointment

from django.contrib import admin

from .admin_site import edc_pharma_admin
from .forms import DispenseAppointmentForm


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
                      ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
                      ModelAdminAuditFieldsMixin, ModelAdminReadOnlyMixin,
                      ModelAdminInstitutionMixin):
    pass


@admin.register(DispenseAppointment, site=edc_pharma_admin)
class DispenseAppointmentAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = DispenseAppointmentForm
