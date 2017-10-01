from edc_base.model_mixins import BaseUuidModel

from django.db import models

from .dispense_schedule import DispenseSchedule


# from ..classes import DispenseTimepointMixin
class DispenseTimepoint(BaseUuidModel):

    timepoint = models.DateField()

    is_dispensed = models.BooleanField(default=False)

    schedule = models.ForeignKey(DispenseSchedule)

    profile_label = models.CharField(max_length=100)

    def previous(self):
        return self.__class__.objects.filter(
            schedule=self.schedule, timepoint__lt=self.timepoint
        ).order_by('timepoint').first()

    def next(self):
        return self.__class__.objects.filter(
            schedule=self.schedule, timepoint__gt=self.timepoint
        ).order_by('timepoint').first()

    def completed(self):
        return self.__class__.objects.filter(
            schedule=self.schedule, is_dispensed=True
        ).order_by('timepoint')

    def next_timepoints(self):
        return self.__class__.objects.filter(
            schedule=self.schedule, timepoint__gt=self.timepoint,
            is_dispensed=False
        ).order_by('timepoint')

    @property
    def print_profile(self):
        from ..dispense_plan import dispense_plans
        control_arm = dispense_plans.get(self.schedule.arm)
        schedule_plan = control_arm.get(self.schedule.name)
        profiles = schedule_plan.get('dispense_profile')
        return profiles.get(self.profile_label.split('.')[0])

    @property
    def profile_medications(self):
        medications = []
        for _, value in self.print_profile.medication_types.items():
            medications.append(value)
        return medications

    def __str__(self):
        return (f'{self.timepoint} - {self.profile_label}')

    class Meta:
        app_label = 'edc_pharma'
