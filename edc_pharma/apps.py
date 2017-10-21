from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig
from edc_appointment.facility import Facility
from edc_base.apps import AppConfig as EdcBaseAppConfigParent
from edc_label.apps import AppConfig as EdcLabelAppConfigParent
import os

from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings


class AppConfig(DjangoAppConfig):
    name = 'edc_pharma'
    country = 'botswana'
    map_area = 'gaborone'
    prescription_model = None
    worklist_model = 'edc_pharma.worklist'
    appointment_model = 'edc_pharma.dispenseappointment'
    template_name = None
    holiday_csv_path = os.path.join(settings.BASE_DIR, 'holidays.csv')
    try:
        prescription_model = settings.EDC_PHARMA_PRESCRIPTION_MODEL
    except AttributeError:
        prescription_model = None

    @property
    def study_site_name(self):
        return 'Gaborone'

    @property
    def site_code(self):
        return '40'

    facilities = {
        'botswana': {'gaborone': Facility(
            name='clinic', days=[MO, TU, WE, TH, FR, SA, SU],
            slots=[100, 100, 100, 100, 100, 100, 100])}}

    @property
    def facility(self):
        return self.facilities.get(
            self.country).get(self.map_area)


class EdcBaseAppConfig(EdcBaseAppConfigParent):
    project_name = 'Edc Pharmacy'
    institution = 'Botswana-Harvard AIDS Institute'


class EdcAppointmentAppConfig(BaseEdcAppointmentAppConfig):
    app_label = 'edc_pharma'
    file_holidays = True


class EdcLabelAppConfig(EdcLabelAppConfigParent):
    default_cups_server_ip = None
    default_printer_label = 'mytest'
    extra_templates_folder = os.path.join(
        settings.STATIC_ROOT, 'edc_pharma', 'label_templates')
