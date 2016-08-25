from django.contrib import admin

from .models import Dispense, Patient, Treatment, Site, Protocol


@admin.register(Dispense)
class DispenseAdmin(admin.ModelAdmin):
    list_display = ('patient', 'treatment', 'frequency_per_day', 'date_prepared',)
    list_filter = ('date_prepared',)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('initials', 'consent_date',)
    list_filter = ('subject_identifier',)


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('treatment_name', 'medium', 'storage_instructions',)
    list_filter = ('treatment_name', 'medium',)


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('protocol', 'site_number', 'telephone_number',)


@admin.register(Protocol)
class ProtocolAdmin(admin.ModelAdmin):
    list_display = ('protocol_number', 'protocol_name',)
