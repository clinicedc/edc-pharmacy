from datetime import datetime, date
from django.db import models
from simple_history.models import HistoricalRecords
from dateutil.relativedelta import relativedelta

from edc_base.model.models import BaseUuidModel

from edc_pharma.models.medication import Medication
from edc_pharma.models.patient import Patient
from edc_pharma.choices import DISPENSE_TYPES, TABLET, SYRUP, IM, IV, SUPPOSITORY, SOLUTION, CAPSULE


class Dispense(BaseUuidModel):

    history = HistoricalRecords()

    date_hierarchy = '-prepared_datetime'

    patient = models.ForeignKey(Patient)

    medication = models.ForeignKey(Medication)

    dispense_type = models.CharField(
        max_length=15,
        choices=DISPENSE_TYPES,
        default=TABLET
    )

    number_of_tablets = models.IntegerField(
        blank=True,
        null=True,
        help_text="Only required if dispense type TABLET, CAPSULES and or SUPPOSITORIES is chosen")

    syrup_dose = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Only required if dispense type SYRUP is chosen")

    times_per_day = models.IntegerField(
        blank=True,
        null=True,
        help_text="Only required if dispense type TABLET, CAPSULES, SUPPOSITORIES,and or SYRUP is chosen")

    total_number_of_tablets = models.IntegerField(
        blank=True,
        null=True,
        help_text="Only required if dispense type TABLET or SUPPOSITORY  is chosen")

    total_dosage_volume = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Only required if dispense type SYRUP, IM, IV is chosen")

    total_volume = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Only required if dispense type IV and or IM is chosen")

    concentration = models.CharField(
        max_length=60,
        blank=True,
        null=True,
        help_text="Only required if dispense type IV, IM, CAPSULES, SOLUTION, SUPPOSITORIES, TABLET is chosen")

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
                '{medication} {dose} dose {times_per_day} times a day '
                '({total_volume})'.format(
                    medication=self.medication.name,
                    syrup_dose=self.syrup_dose,
                    times_per_day=self.times_per_day,
                    total_volume=self.total_volume))
        if self.dispense_type == IV:
            prescription = (
                '{medication} Intravenous {concentration} {duration} '
                '({total_volume})'.format(
                    medication=self.medication.name,
                    iv_duration=self.iv_duration,
                    concentration=self.concentration,
                    times_per_day=self.times_per_day,
                    total_volume=self.total_volume))
        if self.dispense_type == IM:
            prescription = (
                '{medication} IntraMuscular {concentration} {duration} '
                '({total_volume})'.format(
                    medication=self.medication.name,
                    im_duration=self.im_duration,
                    concentration=self.concentration,
                    times_per_day=self.times_per_day,
                    total_volume=self.total_volume))
        if self.dispense_type == SUPPOSITORY:
            prescription = (
                '{medication} {number_of_tablets} suppository {times_per_day} times per day '
                '({total_number_of_tablets} suppository)'.format(
                    medication=self.medication.name,
                    number_of_tablets=self.number_of_tablets,
                    times_per_day=self.times_per_day,
                    total_number_of_tablets=self.total_number_of_tablets))
        if self.dispense_type == CAPSULE:
            prescription = (
                '{medication} {number_of_tablets} capsules {times_per_day} times per day '
                '({total_number_of_tablets} capsules)'.format(
                    medication=self.medication.name,
                    number_of_tablets=self.number_of_tablets,
                    times_per_day=self.times_per_day,
                    total_number_of_tablets=self.total_number_of_tablets))
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
                'number_of_teaspoons': self.dose,
                'total_volume': self.total_volume,
            })
        elif self.dispense_type == IV:
            label_context.update({
                'concentration': self.concentration,
                'total_volume': self.total_volume
            })
        elif self.dispense_type == IM:
            label_context.update({
                'concentration': self.concentration,
                'total_volume': self.total_volume
            })
        elif self.dispense_type == SOLUTION:
            label_context.update({
                'concentration': self.concentration,
                'total_volume': self.total_volume
            })
        elif self.dispense_type == CAPSULE:
            label_context.update({
                'concentration': self.concentration,
                'total_volume': self.total_volume
            })
        elif self.dispense_type == SUPPOSITORY:
            label_context.update({
                'concentration': self.concentration,
                'total_volume': self.total_volume
            })
        return label_context

    class Meta:
        unique_together = (('patient', 'medication', 'prepared_date'), )
