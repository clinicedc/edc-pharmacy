import os

from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings

from edc_base.apps import AppConfig as EdcBaseAppConfigParent
from edc_label.apps import AppConfig as EdcLabelAppConfigParent


class AppConfig(DjangoAppConfig):
    name = 'edc_pharma'
    country = 'botswana'
    dispense_model = None
    try:
        dispense_model = settings.EDC_PHARMA_DISPENSE_MODEL
    except AttributeError:
        dispense_model = None

    @property
    def study_site_name(self):
        return 'Gaborone'

    @property
    def site_code(self):
        return '40'


class EdcBaseAppConfig(EdcBaseAppConfigParent):
    project_name = 'Edc Pharmacy'
    institution = 'Botswana-Harvard AIDS Institute'


class EdcLabelAppConfig(EdcLabelAppConfigParent):
    default_cups_server_ip = None
    default_printer_label = 'mytest'
    extra_templates_folder = os.path.join(
        settings.STATIC_ROOT, 'edc_pharma', 'label_templates')
