from edc_base.model_mixins import BaseUuidModel

from django.db import models

from .dispense_appointment import DispenseAppointment
from .medication_definition import MedicationDefinition


class DispenseHistory(BaseUuidModel):

    dispense_appointment = models.ForeignKey(
        DispenseAppointment)

    dispense_datetime = models.DateTimeField(
        null=True, blank=True)

    weight = models.DecimalField(
        verbose_name='Weight in kg',
        decimal_places=2,
        max_digits=5,
        blank=True,
        null=True)

    duration = models.CharField(max_length=100)

    medication_definition = models.ForeignKey(MedicationDefinition)

    result = models.IntegerField(
        null=True, blank=True)

    def __str__(self):
        return (f'{self.dispense_appointment} - {self.dispense_datetime}')

    class Meta:
        app_label = 'edc_pharma'
