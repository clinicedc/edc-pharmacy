from django.contrib import admin
from django.http.response import HttpResponseRedirect

from edc_base.modeladmin.mixins import (
    ModelAdminBasicMixin, ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminFormInstructionsMixin)

from .admin_site import edc_pharma_admin

from .models import Dispense, Patient, Medication, Site, Protocol


class BaseModelAdmin(ModelAdminBasicMixin, ModelAdminFormAutoNumberMixin, ModelAdminFormInstructionsMixin,
                     ModelAdminAuditFieldsMixin):
    pass


@admin.register(Dispense, site=edc_pharma_admin)
class DispenseAdmin(BaseModelAdmin, admin.ModelAdmin):
    list_display = ('patient', 'medication', 'prepared_datetime',)
    list_filter = ('prepared_datetime',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "patient":
            patient_queryset = Patient.objects.filter(subject_identifier=request.GET.get("patient"))
            if patient_queryset.exists():
                kwargs["queryset"] = patient_queryset
                return super(DispenseAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
            else:
                kwargs["queryset"] = Patient.objects.all()
                return super(DispenseAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_form(self, request, form, change):
        try:
            request.POST['_save_print']
            context = {
                'site': form.instance.patient.site,
                'telephone_number': form.instance.patient.site.telephone_number,
                'patient': form.instance.patient.subject_identifier,
                'initials': form.instance.patient.initials,
                'number_of_tablets': form.instance.number_of_tablets_or_teaspoons,
                'total_tablets_dispensed': form.instance.total_number_of_tablets,
                'sid': form.instance.patient.sid,
                'times_per_day': form.instance.times_per_day,
                'drug_name': form.instance.medication,
                'date_prepared': form.instance.date_prepared.date(),
                'prepared_by': form.instance.user_created,
                'storage_instructions': form.instance.treatment.storage_instructions,
                'protocol': form.instance.treatment.protocol,
            }
            self.print_label("dispense_label", 1, context)
        except KeyError:
            pass
        return admin.ModelAdmin.save_form(self, request, form, change)

    def response_add(self, request, obj, post_url_continue=None):
        next_url = "/?subject_identifier="+str(obj)
        return HttpResponseRedirect(next_url)


@admin.register(Patient, site=edc_pharma_admin)
class PatientAdmin(BaseModelAdmin, admin.ModelAdmin):
    list_display = ('initials', 'consent_datetime',)
    list_filter = ('consent_datetime',)

    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect("/")


@admin.register(Medication, site=edc_pharma_admin)
class MedicationAdmin(BaseModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'storage_instructions',)
    list_filter = ('name', )

    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect("/")


@admin.register(Site, site=edc_pharma_admin)
class SiteAdmin(BaseModelAdmin, admin.ModelAdmin):
    list_display = ('protocol', 'site_code', 'telephone_number',)
    list_filter = ('site_code',)

    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect("/")


@admin.register(Protocol, site=edc_pharma_admin)
class ProtocolAdmin(BaseModelAdmin, admin.ModelAdmin):
    list_display = ('number', 'name',)
    list_filter = ('number',)

    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect("/")
