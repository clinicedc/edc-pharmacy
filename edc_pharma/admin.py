from django.contrib import admin

from .models import Dispense, Patient, Treatment, Site, Protocol

@admin.register(Dispense)
class DispenseAdmin(admin.ModelAdmin):
    list_display = ('patient', 'treatment', 'frequency_per_day', 'date_prepared',)

@admin.register(Patient) 
class PatientAdmin(admin.ModelAdmin):    
    list_display = ('initials', 'consent_date',)

@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):    
    list_display = ('treatment_name', 'medium', 'storage_instructions',)

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):    
    list_display = ('protocol', 'telephone_number',)
