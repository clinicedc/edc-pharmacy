from edc_base.model_mixins import BaseUuidModel

from django.db import models

from edc_search.model_mixins import SearchSlugManager

from ..medications.medication_dosage import MedicationDosage
from ..search_slug_model_mixin import SearchSlugModelMixin
from .dispense_appointment import DispenseAppointment
from .medication_definition import MedicationDefinition


class Manager(SearchSlugManager, models.Manager):
    pass


class Prescription(SearchSlugModelMixin, BaseUuidModel):

    is_approved = models.BooleanField(
        default=False, editable=False)

    dispense_appointment = models.ForeignKey(
        DispenseAppointment)

    dispense_datetime = models.DateTimeField(
        null=True, blank=True)

    description = models.CharField(
        max_length=250,
        null=True, blank=True)

    weight = models.DecimalField(
        verbose_name='Body Weight in Kg',
        decimal_places=2,
        max_digits=5,
        blank=True,
        null=True)

    duration = models.CharField(max_length=100)

    medication_definition = models.ForeignKey(MedicationDefinition)

    result = models.IntegerField(null=True, blank=True)

    is_consented = models.NullBooleanField(
        default=False)

    medication_description = models.CharField(
        max_length=100, null=True, blank=True)

    arm = models.CharField(max_length=100, null=True, blank=True)

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50, null=True, blank=True)

    category = models.CharField(
        max_length=100, null=True, blank=True)

    objects = Manager()

    def __str__(self):
        return (f'{self.dispense_appointment} - {self.dispense_datetime}')

    def save(self, *args, **kwargs):
        self.result = MedicationDosage(
            medication_definition=self.medication_definition,
            weight=self.weight,
            duration=self.duration).required_quantity
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'edc_pharma'
