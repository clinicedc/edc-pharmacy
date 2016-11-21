import factory
import pytz

from datetime import datetime, time, date

from edc_constants.constants import FEMALE

from ..choices import TABLET
from ..models import Patient, Site, Protocol, Medication, Dispense
from django.utils import timezone


class ProtocolFactory(factory.DjangoModelFactory):

    class Meta:
        model = Protocol

    number = '12'
    name = factory.Sequence(lambda n: 'bhp012{0}'.format(n))


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
    storage_instructions = 'Keep at 5° Celsius'


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


class DispenseFactory(factory.DjangoModelFactory):

    class Meta:
        model = Dispense

    patient = factory.SubFactory(PatientFactory)
    medication = factory.SubFactory(MedicationFactory)
    dispense_type = TABLET
    number_of_tablets = 1
    times_per_day = 3
    total_number_of_tablets = 45
    prepared_date = timezone.make_aware(datetime.combine(timezone.now(), time(0, 0, 0)), timezone=pytz.timezone('UTC'))
