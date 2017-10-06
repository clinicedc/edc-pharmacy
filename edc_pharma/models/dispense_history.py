from edc_base.model_mixins import BaseUuidModel

from django.db import models

from .medication import Medication


from.dispense_appointment import DispenseAppointment


class DispenseHistory(BaseUuidModel):

    dispense_appointment = models.ForeignKey(
        DispenseAppointment)

    dispense_datetime = models.DateTimeField()

    medications = models.ManyToManyField(
        Medication,
        verbose_name='Medications dispensed',
        blank=True,
        help_text='')

    def __str__(self):
        return (f'{self.dispense_appointment} - {self.dispense_datetime}')

    class Meta:
        app_label = 'edc_pharma'
