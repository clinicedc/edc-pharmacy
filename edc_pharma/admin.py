from django.contrib import admin

from edc_label.view_mixins import EdcLabelViewMixin
from .models import Dispense, Patient, Treatment, Site, Protocol

from .admin_site import edc_pharma_admin
from .admin_mixin import PrintButtonAdminMixin


@admin.register(Dispense, site=edc_pharma_admin)
class DispenseAdmin(PrintButtonAdminMixin, admin.ModelAdmin):
    
    list_display = ('patient', 'treatment', 'frequency_per_day', 'date_prepared',)
    list_filter = ('date_prepared', 'frequency_per_day',)

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
            #print(context)
            self.print_label("dispense_label", 1, context)
        except KeyError:
            pass
        return admin.ModelAdmin.save_form(self, request, form, change)


@admin.register(Patient, site=edc_pharma_admin)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('initials', 'consent_date',)
    list_filter = ('consent_date',)


@admin.register(Treatment, site=edc_pharma_admin)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('treatment_name', 'medium', 'storage_instructions',)
    list_filter = ('treatment_name', 'medium',)


@admin.register(Site, site=edc_pharma_admin)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('protocol', 'site_number', 'telephone_number',)
    list_filter = ('site_number',)


@admin.register(Protocol, site=edc_pharma_admin)
class ProtocolAdmin(admin.ModelAdmin):
    list_display = ('protocol_number', 'protocol_name',)
    list_filter = ('protocol_number',)
