from django.contrib import admin
from django.http.response import HttpResponseRedirect
from django import forms

from edc_base.modeladmin.mixins import (
    ModelAdminBasicMixin, ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminFormInstructionsMixin)

from .admin_site import edc_pharma_admin

from .models import Dispense, Patient, Medication, Site, Protocol
from edc_pharma.models import TABLET, SYRUP, IV


class BaseModelAdmin(ModelAdminBasicMixin, ModelAdminFormAutoNumberMixin, ModelAdminFormInstructionsMixin,
                     ModelAdminAuditFieldsMixin):
    pass


class DispenseForm(forms.ModelForm):
    def clean(self):
        if self.data['dispense_type'] == TABLET:
            self.validate_tablet()

        elif self.data['dispense_type'] == SYRUP:
            self.validate_syrup()

        elif self.data['dispense_type'] == IV:
            self.validate_iv()

        return self.cleaned_data

    def validate_tablet(self):
        if self.data['number_of_teaspoons']:
            raise forms.ValidationError("You have selected dispense type tablet, you should NOT enter number of teaspoons")
        if not self.data['number_of_tablets']:
            raise forms.ValidationError("You have selected dispense type tablet, you should enter number of tablets")
        if self.data['total_dosage_volume']:
            raise forms.ValidationError("You have selected dispense type tablet, you should NOT enter total dosage volume")
        if self.data['iv_duration']:
            raise forms.ValidationError("You have selected dispense type tablet, you should NOT enter IV duration")
        if not self.data['total_number_of_tablets']:
            raise forms.ValidationError("You have selected dispense type tablet, you should enter total number of tablets")

    def validate_syrup(self):
        if not self.data['number_of_teaspoons']:
            raise forms.ValidationError("You have selected dispense type syrup, you should enter number of teaspoons")
        if self.data['number_of_tablets']:
            raise forms.ValidationError("You have selected dispense type syrup, you should NOT enter number of tablets")
        if self.data['total_number_of_tablets']:
            raise forms.ValidationError("You have selected dispense type syrup, you should NOT enter total number of tablets")
        if not self.data['total_dosage_volume']:
            raise forms.ValidationError("You have selected dispense type syrup, you should enter total dosage volume")
        if self.data['iv_duration']:
            raise forms.ValidationError("You have selected dispense type syrup, you should NOT enter  IV duration")

    def validate_iv(self):
        if self.data['number_of_teaspoons']:
            raise forms.ValidationError("You have selected dispense type IV, you should NOT enter number of teaspoons")
        if self.data['number_of_tablets']:
            raise forms.ValidationError("You have selected dispense type IV, you should NOT enter number of tablets")
        if not self.data['total_dosage_volume']:
            raise forms.ValidationError("You have selected dispense type IV, you should enter total dosage volume")
        if not self.data['iv_duration']:
            raise forms.ValidationError("You have selected dispense type IV, you should enter IV duration")


@admin.register(Dispense, site=edc_pharma_admin)
class DispenseAdmin(BaseModelAdmin, admin.ModelAdmin):
    form = DispenseForm
    list_display = ('patient', 'medication', 'prepared_datetime',)
    list_filter = ('prepared_datetime', 'medication',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "patient":
            patient_queryset = Patient.objects.filter(subject_identifier=request.GET.get("patient"))
            if patient_queryset.exists():
                kwargs["queryset"] = patient_queryset
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
                'storage_instructions': form.instance.medication.storage_instructions,
                'protocol': form.instance.medication.protocol,
            }
            self.print_label("dispense_label", 1, context)
        except KeyError:
            pass
        return admin.ModelAdmin.save_form(self, request, form, change)

    def response_add(self, request, obj, post_url_continue=None):
        next_url = "/?subject_identifier=" + str(obj.patient.subject_identifier)
        return HttpResponseRedirect(next_url)


@admin.register(Patient, site=edc_pharma_admin)
class PatientAdmin(BaseModelAdmin, admin.ModelAdmin):
    list_display = ('initials', 'consent_datetime',)
    list_filter = ('consent_datetime',)

    def response_add(self, request, obj, post_url_continue=None):
        next_url = "/?subject_identifier=" + str(obj.subject_identifier)
        return HttpResponseRedirect(next_url)


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
