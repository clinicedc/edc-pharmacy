from edc_base.model_mixins import BaseUuidModel
from edc_pharma.constants import NEW, SCHEDULE_STATUS

from django.db import models


class DispenseSchedule(BaseUuidModel):

    status = models.CharField(
        verbose_name=('Status'),
        choices=SCHEDULE_STATUS,
        max_length=25,
        default=NEW)

    subject_identifier = models.CharField(
        max_length=150,)

    arm = models.CharField(max_length=100,)

    name = models.CharField(max_length=100,)

    sequence = models.IntegerField()

    duration = models.CharField(max_length=100,)

    description = models.CharField(
        max_length=100, null=True, blank=True)

    start_datetime = models.DateField()

    end_datetime = models.DateField()

    def next(self):
        return self.__class__.objects.filter(
            subject_identifier=self.subject_identifier,
            sequence__gt=self.sequence).order_by('created').first()

    def previous(self):
        return self.__class__.objects.filter(
            subject_identifier=self.subject_identifier,
            sequence__lt=self.sequence).order_by('-created').first()

    def __str__(self):
        return (f'{self.subject_identifier}@{self.name}.'
                f' from {self.start_date} to {self.end_date}')

    class Meta:
        app_label = 'edc_pharma'
