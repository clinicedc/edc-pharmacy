import factory

from datetime import date
from django.utils import timezone
from edc_constants.constants import FEMALE
from edc_pharma.models import Patient, Site, Protocol, Medication


class ProtocolFactory(factory.DjangoModelFactory):

    class Meta:
        model = Protocol

    number = '12'
    name = 'bhp012'


class SiteFactory(factory.DjangoModelFactory):

    class Meta:
        model = Site

    protocol = factory.SubFactory(ProtocolFactory)
    site_code = 'BHP009'
    telephone_number = '3456765'


class MedicationFactory(factory.DjangoModelFactory):

    class Meta:
        model = Medication

    name = 'AZT'
    protocol = factory.SubFactory(ProtocolFactory)
    storage_instructions = 'Keep at 5deg Celsius'


class PatientFactory(factory.DjangoModelFactory):

    class Meta:
        model = Patient

    subject_identifier = '12345'
    initials = 'KK'
    gender = FEMALE
    dob = date(1988, 7, 7)
    sid = 'A2345'
    consent_datetime = timezone.now()
    site = factory.SubFactory(SiteFactory)
