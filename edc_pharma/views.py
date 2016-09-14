import json

from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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


class HomeView(EdcBaseViewMixin, EdcLabelViewMixin, FormView):

    template_name = 'edc_pharma/home.html'
    form_class = PatientForm
    paginate_by = 3

    def get_success_url(self):
        return reverse('home_url')

    def form_valid(self, form):
        if form.is_valid():
            context = self.get_context_data()
            subject_identifier = form.cleaned_data['subject_identifier']
            patient = self.patient(subject_identifier)
            if not patient:
                form.add_error('subject_identifier', 'Patient not found. Try again.')
            context.update({
                'dispenses': self.dispenses(patient),
                'patient': patient,
                'form': form})
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        if self.kwargs.get('dispense_pk'):
            dispense = Dispense.objects.get(pk=self.kwargs.get('dispense_pk'))
            self.print_label("dispense_label", 1, dispense.label_context)
        patient = self.patient(kwargs.get('subject_identifier'))
        context.update({
            'dispenses': self.dispenses(patient),
            'patient': patient})
        return context

    def patient(self, subject_identifier):
        try:
            patient = Patient.objects.get(subject_identifier=subject_identifier)
        except Patient.DoesNotExist:
            patient = None
        return patient

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
