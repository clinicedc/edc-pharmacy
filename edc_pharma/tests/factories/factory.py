import factory

from datetime import date
from edc_constants.constants import FEMALE

from edc_pharma.models.patient import Patient
from edc_pharma.models.site import Site
from edc_pharma.models.protocol import Protocol
from edc_pharma.models.medication import Medication
from edc_pharma.models.dispense import Dispense
from edc_pharma.choices import TABLET


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
    consent_date = date.today()
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
    prepared_date = date.today()
