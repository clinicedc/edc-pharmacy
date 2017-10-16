from edc_base.model_mixins import BaseUuidModel

from django.db import models

from .dispense_appointment_mixin import DispenseAppointmentMixin
from .dispense_schedule import DispenseSchedule


class DispenseAppointment(DispenseAppointmentMixin, BaseUuidModel):

    is_dispensed = models.BooleanField(default=False, editable=False)

    schedule = models.ForeignKey(DispenseSchedule)

    profile_label = models.CharField(max_length=100)

    def __str__(self):
        return (f'{self.appt_datetime} - {self.profile_label}')

    class Meta:
        app_label = 'edc_pharma'
