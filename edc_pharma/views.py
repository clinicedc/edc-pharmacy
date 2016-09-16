import json

from urllib.parse import urlencode 

from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from edc_base.views.edc_base_view_mixin import EdcBaseViewMixin
from edc_label.view_mixins import EdcLabelViewMixin

from .models import Dispense, Patient
from django.contrib.admin.templatetags.admin_list import pagination
from django.template.context_processors import request
from django.core import paginator
from edc_pharma.forms import PatientForm
from django.views.generic.edit import FormView
from django.urls.base import reverse
from edc_pharma.models import TABLET, SYRUP, IV
from edc_base.model.constants import DEFAULT_BASE_FIELDS
from test.test_socketserver import receive


class HomeView(EdcBaseViewMixin, EdcLabelViewMixin, FormView):

    template_name = 'edc_pharma/home.html'
    form_class = PatientForm
    paginate_by = 3
    number_of_copies = 1

    def get_success_url(self):
        return reverse('home_url')

    def form_valid(self, form):
        if form.is_valid():
            context = self.get_context_data()
            subject_identifier = form.cleaned_data['subject_identifier']
            patient = self.patient(subject_identifier)
            if not patient:
                form.add_error('subject_identifier', 'Patient not found. Try again.')
            else:
                recent_dispense = self.get_recent_dispensing(patient)
                if recent_dispense:
                    recent_dispense_patient_id = recent_dispense.patient.id
                    recent_dispense_medication_id = recent_dispense.medication.id
                    recent_dispense = {field: value for field, value in recent_dispense.__dict__.items() if field not in DEFAULT_BASE_FIELDS + ['prepared_datetime'] + ['medication_id'] + ['patient_id'] and value is not None}
                    recent_dispense.update({'patient': recent_dispense_patient_id, 'medication': recent_dispense_medication_id})
                context.update({'recent_dispense_querystring': urlencode(recent_dispense)})
            context.update({
                'dispenses': self.dispenses(patient),
                'patient': patient,
                'form': form})
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        if self.kwargs.get('dispense_pk'):
            dispense = Dispense.objects.get(pk=self.kwargs.get('dispense_pk'))
            dispense_type = self.get_dispense_type(dispense)
            self.print_label(dispense_type, self.number_of_copies, dispense.label_context)
        patient = self.patient(kwargs.get('subject_identifier'))
        context.update({
            'dispenses': self.dispenses(patient),
            'patient': patient})
        return context

    def get_dispense_type(self, dispense):
        if dispense.dispense_type == TABLET:
            return "dispense_label_tablet"
        elif dispense.dispense_type == SYRUP:
            return "dispense_label_syrup"
        elif dispense.dispense_type == IV:
            return "dispense_label_iv"

    def patient(self, subject_identifier):
        try:
            patient = Patient.objects.get(subject_identifier=subject_identifier)
        except Patient.DoesNotExist:
            patient = None
        return patient

    def get_recent_dispensing(self, patient):
        try:
            recent_dispense = Dispense.objects.filter(patient=patient).order_by("-prepared_datetime")
            if recent_dispense:
                recent_dispense = recent_dispense[0]
        except Dispense.DoesNotExist:
            recent_dispense = {'patient': None, 'medication': None}
        return recent_dispense

    def dispenses(self, patient):
        """Returns a dispense queryset after pagination."""
        dispenses = Dispense.objects.filter(patient=patient).order_by("-prepared_datetime")
        paginator = Paginator(dispenses, self.paginate_by)
        try:
            dispenses = paginator.page(self.kwargs.get('page', 1))
        except EmptyPage:
            dispenses = paginator.page(paginator.num_pages)
        return dispenses

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)