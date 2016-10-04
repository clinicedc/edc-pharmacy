from datetime import datetime, date
from django.core.validators import RegexValidator
from django.db import models
from simple_history.models import HistoricalRecords

from edc_base.model.models import BaseUuidModel
from edc_constants.choices import GENDER
from edc_base.model.validators.date import date_not_future
from edc_base.utils.age import formatted_age
from dateutil.relativedelta import relativedelta

TABLET = 'TABLET'
SYRUP = 'SYRUP'
IV = 'IV'
DISPENSE_TYPES = (
    (TABLET, 'TABLET'),
    (SYRUP, 'SYRUP'),
    (IV, 'IV'),
)


class Protocol(BaseUuidModel):

    number = models.CharField(max_length=30)

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.number


class Site(BaseUuidModel):

    protocol = models.ForeignKey(Protocol)

    site_code = models.CharField(
        max_length=20,
        validators=[RegexValidator('[\d]+', 'Invalid format.')])

    telephone_number = models.CharField(
        max_length=7,
        validators=[RegexValidator('^[2-8]{1}[0-9]{6}$', 'Invalid format.')])

    def __str__(self):
        return self.site_code


class Patient(BaseUuidModel):

    subject_identifier = models.CharField(max_length=20)

    initials = models.CharField(
        max_length=5,
        validators=[RegexValidator('[A-Z]{2,3}', message='Use CAPS, 2-3 letters')],
        help_text='Format is AA or AAA')

    gender = models.CharField(
        max_length=10,
        choices=GENDER)

    dob = models.DateField(
        blank=True,
        null=True,
        validators=[date_not_future])

    sid = models.CharField(
        max_length=20,
        validators=[RegexValidator('[\d]+', 'Invalid format.')],
    )

    consent_datetime = models.DateTimeField()

    site = models.ForeignKey(Site)

    history = HistoricalRecords()

    def __str__(self):
        return '{}, ({}), Site {}'.format(self.subject_identifier, self.initials, self.site.site_code)

    @property
    def born(self):
        return self.dob.strftime('%Y-%m-%d')

    @property
    def age(self):
        return formatted_age(self.dob, date.today())


class Medication(BaseUuidModel):

    name = models.CharField(max_length=200)

    protocol = models.ForeignKey(Protocol)

    storage_instructions = models.TextField(max_length=200)

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'edc_pharma'


class Dispense(BaseUuidModel):

    date_hierarchy = '-prepared_datetime'

    patient = models.ForeignKey(Patient)

    medication = models.ForeignKey(Medication)

    dispense_type = models.CharField(
        max_length=8,
        choices=DISPENSE_TYPES,
        default=TABLET
    )

    number_of_tablets = models.IntegerField(
        blank=True,
        null=True,
        help_text="Only required if dispense type TABLET is chosen")

    syrup_volume = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Only required if dispense type SYRUP is chosen")

    times_per_day = models.IntegerField(
        blank=True,
        null=True,
        help_text="Only required if dispense type TABLET or SYRUP is chosen")

    total_number_of_tablets = models.IntegerField(
        blank=True,
        null=True,
        help_text="Only required if dispense type TABLET is chosen")

    total_dosage_volume = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Only required if dispense type SYRUP or IV is chosen")

    iv_concentration = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Only required if dispense type IV is chosen")

    iv_duration = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Only required if dispense type IV is chosen")

    prepared_datetime = models.DateTimeField(default=datetime.now)

    prepared_date = models.DateTimeField(default=date.today, editable=False)

    def __str__(self):
        return str(self.patient)

    @property
    def refill_date(self):
        refill_date = None
        if self.dispense_type == TABLET:
            days = self.total_number_of_tablets / (self.times_per_day * self.number_of_tablets)
            refill_date = date.today() + relativedelta(days=days + 1)
        return refill_date

    @property
    def prescription(self):
        if self.dispense_type == TABLET:
            if self.number_of_tablets > 1:
                prescription = (
                    '{medication} {number_of_tablets} tablets {times_per_day} times per day '
                    '({total_number_of_tablets} tablets)'.format(
                        medication=self.medication.name,
                        number_of_tablets=self.number_of_tablets,
                        times_per_day=self.times_per_day,
                        total_number_of_tablets=self.total_number_of_tablets))
            else:
                prescription = (
                    '{medication} 1 tablet {times_per_day} times per day '
                    '({total_number_of_tablets} tablets)'.format(
                        medication=self.medication.name,
                        times_per_day=self.times_per_day,
                        total_number_of_tablets=self.total_number_of_tablets))
        if self.dispense_type == SYRUP:
            prescription = (
                '{medication} {syrup_volume} volume {times_per_day} times a day '
                '({total_dosage_volume})'.format(
                    medication=self.medication.name,
                    syrup_volume=self.syrup_volume,
                    times_per_day=self.times_per_day,
                    total_dosage_volume=self.total_dosage_volume))
        if self.dispense_type == IV:
            prescription = (
                '{medication} Intravenous {iv_concentration} {iv_duration} '
                '({total_dosage_volume})'.format(
                    medication=self.medication.name,
                    iv_duration=self.iv_duration,
                    iv_concentration=self.iv_concentration,
                    times_per_day=self.times_per_day,
                    total_dosage_volume=self.total_dosage_volume))
        return prescription

    @property
    def label_context(self):
        label_context = {
            'site': self.patient.site,
            'telephone_number': self.patient.site.telephone_number,
            'patient': self.patient.subject_identifier,
            'initials': self.patient.initials,
            'sid': self.patient.sid,
            'times_per_day': self.times_per_day,
            'drug_name': self.medication,
            'prepared_datetime': self.prepared_datetime.strftime("%d-%m-%y %H:%M"),
            'prepared_by': self.user_created,
            'storage_instructions': self.medication.storage_instructions,
            'protocol': self.medication.protocol,
        }
        if self.dispense_type == TABLET:
            label_context.update({
                'number_of_tablets': self.number_of_tablets,
                'total_number_of_tablets': self.total_number_of_tablets,
            })
        elif self.dispense_type == SYRUP:
            label_context.update({
                'number_of_teaspoons': self.syrup_volume,
                'total_dosage_volume': self.total_dosage_volume,
            })
        elif self.dispense_type == IV:
            label_context.update({
                'concentration': self.iv_concentration,
                'total_dosage_volume': self.total_dosage_volume
            })
        return label_context

    class Meta:
        unique_together = (('patient', 'medication', 'prepared_date'), )
