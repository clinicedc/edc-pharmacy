from edc_base.model_fields.custom_fields import InitialsField
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
        verbose_name='Approved?',
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

    clinician_initials = InitialsField(
        verbose_name='Clinician initial',
        default='--',
    )

    initials = InitialsField(
        verbose_name='Subject initial',
        default='--',
    )

    duration = models.CharField(
        verbose_name='Duration for prescription',
        max_length=100)

    medication_definition = models.ForeignKey(MedicationDefinition)

    result = models.IntegerField(
        verbose_name='Auto calculated required quantity',
        null=True, blank=True)

    recommanded_result = models.IntegerField(
        verbose_name='Recommand required quantity',
        null=True, blank=True)

    is_consented = models.NullBooleanField(
        verbose_name='Is the consent completed?',
        default=False)

    medication_description = models.CharField(
        verbose_name='Prescription Description',
        max_length=100, null=True, blank=True)

    arm = models.CharField(
        verbose_name='Randomization Arm',
        max_length=100, null=True, blank=True)

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50, null=True, blank=True)

    category = models.CharField(
        verbose_name='Prescription category (Capsule or Vials).',
        max_length=100, null=True, blank=True)

    objects = Manager()

    def __str__(self):
        return (f'{self.dispense_appointment} - {self.dispense_datetime}')

    def save(self, *args, **kwargs):
        if not self.id:
            self.result = MedicationDosage(
                medication_definition=self.medication_definition,
                weight=self.weight,
                duration=self.duration).required_quantity
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'edc_pharma'
