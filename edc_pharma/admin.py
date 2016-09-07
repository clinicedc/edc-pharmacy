from django.contrib import admin

from edc_base.modeladmin.mixins import (
    ModelAdminBasicMixin, ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminFormInstructionsMixin)
from edc_label.view_mixins import EdcLabelMixin

from .admin_site import edc_pharma_admin
from .models import Dispense, Patient, Treatment, Site, Protocol


class BaseModelAdmin(ModelAdminBasicMixin, ModelAdminFormAutoNumberMixin, ModelAdminFormInstructionsMixin,
                     ModelAdminAuditFieldsMixin):
    pass


@admin.register(Dispense, site=edc_pharma_admin)
class DispenseAdmin(BaseModelAdmin, EdcLabelMixin, admin.ModelAdmin):
    list_display = ('patient', 'treatment', 'prepared_datetime',)
    list_filter = ('prepared_datetime',)

    def save_form(self, request, form, change):
        try:
            request.POST['_save_print']
            context = {
                'site': form.instance.patient.site,
                'telephone_number': form.instance.patient.site.telephone_number,
                'patient': form.instance.patient.subject_identifier,
                'initials': form.instance.patient.initials,
                'dosage': form.instance.dose_amount,
                'frequency': form.instance.frequency_per_day,
                'prepared_datetime': form.instance.prepared_datetime,
                'prepared_by': form.instance.user_created,
                'storage_instructions': form.instance.treatment.storage_instructions,
                'protocol': form.instance.treatment.protocol
            }
            self.print_label("dispense_label", 1, context)
        except KeyError:
            pass
        return admin.ModelAdmin.save_form(self, request, form, change)


@admin.register(Patient, site=edc_pharma_admin)
class PatientAdmin(BaseModelAdmin, admin.ModelAdmin):
    list_display = ('initials', 'consent_datetime',)
    list_filter = ('consent_datetime',)


@admin.register(Treatment, site=edc_pharma_admin)
class TreatmentAdmin(BaseModelAdmin, admin.ModelAdmin):
    list_display = ('treatment_name', 'storage_instructions',)
    list_filter = ('treatment_name', )


@admin.register(Site, site=edc_pharma_admin)
class SiteAdmin(BaseModelAdmin, admin.ModelAdmin):
    list_display = ('protocol', 'site_code', 'telephone_number',)
    list_filter = ('site_code',)


@admin.register(Protocol, site=edc_pharma_admin)
class ProtocolAdmin(BaseModelAdmin, admin.ModelAdmin):
    list_display = ('protocol_number', 'protocol_name',)
    list_filter = ('protocol_number',)
