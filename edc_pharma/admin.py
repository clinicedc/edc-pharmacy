from django.contrib import admin

from .models import Dispense, Patient, Treatment, Site, Protocol

from .admin_site import edc_pharma_admin
from edc_base.modeladmin.mixins import ModelAdminBasicMixin,\
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,\
    ModelAdminFormInstructionsMixin


class BaseModelAdmin(ModelAdminBasicMixin, ModelAdminFormAutoNumberMixin, ModelAdminFormInstructionsMixin,
                     ModelAdminAuditFieldsMixin):
    pass


@admin.register(Dispense, site=edc_pharma_admin)
class DispenseAdmin(BaseModelAdmin, admin.ModelAdmin):
    list_display = ('patient', 'treatment', 'date_prepared',)
    list_filter = ('date_prepared',)


@admin.register(Patient, site=edc_pharma_admin)
class PatientAdmin(BaseModelAdmin, admin.ModelAdmin):
    list_display = ('initials', 'consent_date',)
    list_filter = ('consent_date',)


@admin.register(Treatment, site=edc_pharma_admin)
class TreatmentAdmin(BaseModelAdmin, admin.ModelAdmin):
    list_display = ('treatment_name', 'storage_instructions',)
    list_filter = ('treatment_name', )


@admin.register(Site, site=edc_pharma_admin)
class SiteAdmin(BaseModelAdmin, admin.ModelAdmin):
    list_display = ('protocol', 'site_number', 'telephone_number',)
    list_filter = ('site_number',)


@admin.register(Protocol, site=edc_pharma_admin)
class ProtocolAdmin(BaseModelAdmin, admin.ModelAdmin):
    list_display = ('protocol_number', 'protocol_name',)
    list_filter = ('protocol_number',)
