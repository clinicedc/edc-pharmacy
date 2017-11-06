import os

from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings
from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig
from edc_base.apps import AppConfig as BaseEdcBaseAppConfig
from edc_facility.apps import AppConfig as BaseEdcFacilityAppConfig
from edc_label.apps import AppConfig as BaseEdcLabelAppConfig


class AppConfig(DjangoAppConfig):
    name = 'edc_pharmacy'
    prescription_model = 'edc_pharmacy.prescription'
    worklist_model = 'edc_pharmacy.worklist'
    template_name = None

    @property
    def study_site_name(self):
        return 'Gaborone'

    @property
    def site_code(self):
        return '40'

    @property
    def facility(self):
        return self.facilities.get(
            self.country).get(self.map_area)


if settings.APP_NAME == 'edc_pharmacy':

    class EdcAppointmentAppConfig(BaseEdcAppointmentAppConfig):
        appointment_model = 'edc_pharmacy.appointment'

    class EdcFacilityAppConfig(BaseEdcFacilityAppConfig):
        definitions = {
            'gaborone': dict(
                name='clinic', days=[MO, TU, WE, TH, FR, SA, SU],
                slots=[100, 100, 100, 100, 100, 100, 100])}

    class EdcBaseAppConfig(BaseEdcBaseAppConfig):
        project_name = 'Edc Pharmacy'
        institution = 'Botswana-Harvard AIDS Institute'

    class EdcLabelAppConfig(BaseEdcLabelAppConfig):
        default_cups_server_ip = None
        default_printer_label = 'mytest'
        extra_templates_folder = os.path.join(
            settings.STATIC_ROOT, 'edc_pharmacy', 'label_templates')
