from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_base.modeladmin_mixins import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminReadOnlyMixin, ModelAdminInstitutionMixin)
from edc_pharma.models.dispense_timepoint import DispenseTimepoint

from django.contrib import admin

from .admin_site import edc_pharma_admin
from .forms import DispenseTimepointForm


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
                      ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
                      ModelAdminAuditFieldsMixin, ModelAdminReadOnlyMixin,
                      ModelAdminInstitutionMixin):
    pass


@admin.register(DispenseTimepoint, site=edc_pharma_admin)
class DispenseTimepointAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = DispenseTimepointForm
