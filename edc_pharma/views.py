import json

from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from edc_base.views.edc_base_view_mixin import EdcBaseViewMixin
from edc_label.view_mixins import EdcLabelViewMixin

from .models import Dispense, Patient


class HomeView(EdcBaseViewMixin, EdcLabelViewMixin, TemplateView):

    template_name = 'edc_pharma/home.html'

    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        if self.kwargs.get('dispense_pk'):
            dispense = Dispense.objects.get(pk=self.kwargs.get('dispense_pk'))
            self.print_label("dispense_label", 1, dispense.label_context)
        try:
            patient = Patient.objects.get(subject_identifier=self.request.GET.get("subject_identifier"))
            dispenses = Dispense.objects.filter(patient=patient)
        except Patient.DoesNotExist:
            patient = None
            dispenses = None
        context.update({
            'dispenses': dispenses,
            'patient': patient})
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)
