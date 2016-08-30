import json

from django.views.generic.base import TemplateView

from edc_base.views.edc_base_view_mixin import EdcBaseViewMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.apps import apps as django_apps
from django.http.response import HttpResponse
from django.views.generic.base import TemplateView
from edc_label.label import app_config, Label
from edc_label.print_server import PrintServer
from django.core import serializers

from .models import Dispense, Patient, Treatment, Site, Protocol


class HomeView(EdcBaseViewMixin, TemplateView):

    template_name = 'edc_pharma/home.html'
    print_server_error = None

    def __init__(self, **kwargs):
        self._print_server = None
        self._printers = {}
        self.cups_server_ip = app_config.default_cups_server_ip
        self.printer_label = app_config.default_printer_label
        super(HomeView, self).__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)

    def get_dispense_data(self):
        json_serializer = serializers.get_serializer("json")()
        dispense_data = json_serializer.serialize(Dispense.objects.all().order_by('id')[:5], ensure_ascii=False)
        return HttpResponse(request, "home.html", {'dispense_label': dispense_data})