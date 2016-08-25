from django.apps import AppConfig as DjangoAppConfig

from edc_base.apps import AppConfig as EdcBaseAppConfigParent


class AppConfig(DjangoAppConfig):
    name = 'edc_pharma'


class EdcBaseAppConfig(EdcBaseAppConfigParent):
    project_name = 'Edc Pharmacy'
    institution = 'Botswana-Harvard AIDS Institute'
