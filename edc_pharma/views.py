import json

from django.views.generic.base import TemplateView

from edc_base.views.edc_base_view_mixin import EdcBaseViewMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.apps import apps as django_apps
from django.http.response import HttpResponse
from django.views.generic.base import TemplateView
from edc_label.view_mixins import EdcLabelViewMixin


from .models import Dispense, Patient, Treatment, Site, Protocol


class HomeView(EdcBaseViewMixin, EdcLabelViewMixin, TemplateView):

    template_name = 'edc_pharma/home.html'
    print_server_error = None

    paginate_by = 10

    def __init__(self, **kwargs):
        self._print_server = None
        self._printers = {}
        self.cups_server_ip = app_config.default_cups_server_ip
        self.printer_label = app_config.default_printer_label
        super(HomeView, self).__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        subject_identifier = self.request.GET.get("subject_identifier")
        dispenses = Dispense.objects.filter(
            patient__subject_identifier=subject_identifier).order_by('date_prepared')
        print(dispenses)
        context.update({'dispenses': dispenses})
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)
    
    

