from edc_base.model_mixins import BaseUuidModel

from django.db import models

from edc_search.model_mixins import SearchSlugManager
from ..search_slug_model_mixin import SearchSlugModelMixin

from .dispense_appointment_mixin import DispenseAppointmentMixin
from .dispense_schedule import DispenseSchedule


class Manager(SearchSlugManager, models.Manager):
    pass


class DispenseAppointment(SearchSlugModelMixin, DispenseAppointmentMixin, BaseUuidModel):

    is_dispensed = models.BooleanField(default=False, editable=False)

    schedule = models.ForeignKey(DispenseSchedule)

    profile_label = models.CharField(max_length=100)

    objects = Manager()

    def __str__(self):
        return (f'{self.appt_datetime} - {self.profile_label}')

    class Meta:
        app_label = 'edc_pharma'
