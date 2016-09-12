import json

from django.shortcuts import render_to_response, get_object_or_404
from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from edc_base.views.edc_base_view_mixin import EdcBaseViewMixin
from edc_label.view_mixins import EdcLabelViewMixin

from .models import Dispense
from .models import Patient
from edc_pharma.models import TABLET


class HomeView(EdcBaseViewMixin, EdcLabelViewMixin, TemplateView):

    template_name = 'edc_pharma/home.html'

    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        subject_identifier = self.request.GET.get("subject_identifier")
        patient_data = Patient.objects.filter(subject_identifier=subject_identifier)
        dispenses = Dispense.objects.filter(
            patient__subject_identifier=subject_identifier)
        if patient_data.exists():
            context.update({'patient_exists': True})
            if dispenses.exists():
                context.update({'dispenses': dispenses})
                patient_data = patient_data.values()[0]
                context.update(patient_data)
                return context
            else:
                return context
        else:
            context.update({'patient_exists': False})
            return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if 'pk' in request.GET:
            dispense_id = self.request.GET.get("pk")
            dispense_data = Dispense.objects.get(pk=dispense_id)

            if dispense_data.dispense_type == TABLET:
                context = {
                    'site': dispense_data.patient.site,
                    'telephone_number': dispense_data.patient.site.telephone_number,
                    'patient': dispense_data.patient.subject_identifier,
                    'initials': dispense_data.patient.initials,
                    'number_of_tablets': dispense_data.number_of_tablets_or_teaspoons,
                    'total_tablets_dispensed': dispense_data.total_number_of_tablets,
                    'sid': dispense_data.patient.sid,
                    'times_per_day': dispense_data.times_per_day,
                    'drug_name': dispense_data.medication,
                    'prepared_datetime': dispense_data.prepared_datetime.date(),
                    'prepared_by': dispense_data.user_created,
                    'storage_instructions': dispense_data.medication.storage_instructions,
                    'protocol': dispense_data.medication.protocol,
                }
                context.update(context)
                print(context)
                self.print_label("dispense_label", 1, context)
                return self.render_to_response(context)

            else:
                context = {
                    'site': dispense_data.patient.site,
                    'telephone_number': dispense_data.patient.site.telephone_number,
                    'patient': dispense_data.patient.subject_identifier,
                    'initials': dispense_data.patient.initials,
                    'number_of_teaspoons': dispense_data.number_of_tablets_or_teaspoons,
                    'quantity_dispensed': dispense_data.total_dosage_volume,
                    'sid': dispense_data.patient.sid,
                    'times_per_day': dispense_data.times_per_day,
                    'drug_name': dispense_data.medication,
                    'prepared_datetime': dispense_data.prepared_datetime.date(),
                    'prepared_by': dispense_data.user_created,
                    'storage_instructions': dispense_data.medication.storage_instructions,
                    'protocol': dispense_data.medication.protocol,
                }
                context.update(context)
                print(context)
                self.print_label("dispense_label_syrup", 1, context)
                return self.render_to_response(context)
        else:
            return self.render_to_response(context)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)
