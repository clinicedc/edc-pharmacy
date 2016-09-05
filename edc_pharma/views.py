import json

from django.views.generic.base import TemplateView

from edc_base.views.edc_base_view_mixin import EdcBaseViewMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.apps import apps as django_apps
from django.http.response import HttpResponse
from django.views.generic.base import TemplateView
from edc_label.view_mixins import EdcLabelViewMixin

from .models import Dispense


class HomeView(EdcBaseViewMixin, EdcLabelViewMixin, TemplateView):

    template_name = 'edc_pharma/home.html'

    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        subject_identifier = self.request.GET.get("subject_identifier")
        dispenses = Dispense.objects.filter(
            patient__subject_identifier=subject_identifier).order_by('date_prepared')
        context.update({'dispenses': dispenses})
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if 'pk' in request.GET:
            dispense_id = self.request.GET.get("pk")
            dispense_data = Dispense.objects.get(pk=dispense_id)

            context = {
                'site': dispense_data.patient.site,
                'telephone_number': dispense_data.patient.site.telephone_number,
                'patient': dispense_data.patient.subject_identifier,
                'initials': dispense_data.patient.initials,
                'dosage': dispense_data.dose_amount,
                'frequency': dispense_data.frequency_per_day,
                'date_prepared': dispense_data.date_prepared,
                'prepared_by': dispense_data.user_created,
                'storage_instructions': dispense_data.treatment.storage_instructions,
                'protocol': dispense_data.treatment.protocol
            }

            print(context)

            context.update(context)
            self.print_label("dispense_label")

        else:
            return self.render_to_response(context)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)
