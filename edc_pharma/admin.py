from django.contrib import admin

from .models import Dispense, Patient, Treatment, Site, Protocol

from .admin_site import edc_pharma_admin


@admin.register(Dispense, site=edc_pharma_admin)
class DispenseAdmin(admin.ModelAdmin):
    list_display = ('patient', 'treatment', 'frequency_per_day', 'date_prepared',)
    list_filter = ('date_prepared', 'frequency_per_day',)


@admin.register(Patient, site=edc_pharma_admin)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('initials', 'consent_date',)
    list_filter = ('subject_identifier',)


@admin.register(Treatment, site=edc_pharma_admin)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('treatment_name', 'medium', 'storage_instructions',)
    list_filter = ('treatment_name', 'medium',)


@admin.register(Site, site=edc_pharma_admin)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('protocol', 'site_number', 'telephone_number',)


@admin.register(Protocol, site=edc_pharma_admin)
class ProtocolAdmin(admin.ModelAdmin):
    list_display = ('protocol_number', 'protocol_name',)
