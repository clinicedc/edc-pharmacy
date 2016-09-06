from django.contrib import admin

from edc_label.view_mixins import EdcLabelViewMixin
from .models import Dispense, Patient, Treatment, Site, Protocol

from .admin_site import edc_pharma_admin
from .admin_mixin import PrintButtonAdminMixin
from edc_base.modeladmin.mixins import ModelAdminBasicMixin,\
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,\
    ModelAdminFormInstructionsMixin


class BaseModelAdmin(ModelAdminBasicMixin, ModelAdminFormAutoNumberMixin, ModelAdminFormInstructionsMixin,
                     ModelAdminAuditFieldsMixin):
    pass


@admin.register(Dispense, site=edc_pharma_admin)
class DispenseAdmin(BaseModelAdmin, admin.ModelAdmin, PrintButtonAdminMixin):
    list_display = ('patient', 'treatment', 'date_prepared',)
    list_filter = ('date_prepared',)

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
                'date_prepared': form.instance.date_prepared,
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
