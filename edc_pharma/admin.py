from django.contrib import admin
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse

from edc_base.modeladmin.mixins import (
    ModelAdminBasicMixin, ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminFormInstructionsMixin, ModelAdminRedirectMixin)

from .admin_site import edc_pharma_admin

from .models import Dispense, Patient, Medication, Site, Protocol
from edc_pharma.forms import DispenseForm


class BaseModelAdmin(ModelAdminBasicMixin, ModelAdminFormAutoNumberMixin, ModelAdminFormInstructionsMixin,
                     ModelAdminAuditFieldsMixin, ModelAdminRedirectMixin):
    pass


@admin.register(Dispense, site=edc_pharma_admin)
class DispenseAdmin(BaseModelAdmin, admin.ModelAdmin):
    form = DispenseForm
    list_display = ('patient', 'medication', 'prepared_datetime',)
    list_filter = ('prepared_datetime', 'medication',)

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
                'storage_instructions': form.instance.medication.storage_instructions,
                'protocol': form.instance.medication.protocol,
            }
            self.print_label("dispense_label", 1, context)
        except KeyError:
            pass
        return admin.ModelAdmin.save_form(self, request, form, change)

    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect(reverse('home_url', kwargs={'subject_identifier': str(obj.patient.subject_identifier)}))


@admin.register(Patient, site=edc_pharma_admin)
class PatientAdmin(BaseModelAdmin, admin.ModelAdmin):
    list_display = ('initials', 'consent_datetime',)
    list_filter = ('consent_datetime',)

    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect(reverse('home_url', kwargs={'subject_identifier': str(obj.subject_identifier)}))


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
