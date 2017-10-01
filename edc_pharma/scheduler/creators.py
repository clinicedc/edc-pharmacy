from ..models import DispenseSchedule, DispenseTimepoint
from ..print_profile import DispenseProfileSelector


class DispenseTimepointCreator:

    """Creates dispense timepoints and update.
    """

    profile_selector_cls = DispenseProfileSelector

    def __init__(self, schedule_name=None, schedule_plan=None,
                 subject_identifier=None, schedule=None, timepoints=None):
        self.schedule = schedule
        self.schedule_name = schedule_name
        self.schedule_plan = schedule_plan
        self.subject_identifier = subject_identifier
        self.timepoints = timepoints

    def create(self):
        profile_selector = self.profile_selector_cls(
            subject_identifier=self.subject_identifier,
            schedule_name=self.schedule_name,
            schedule_plan=self.schedule_plan)
        for code in self.timepoints:
            timepoint = self.timepoints.get(code)
            try:
                DispenseTimepoint.objects.get(
                    schedule=self.schedule,
                    timepoint=timepoint.timepoint_datetime,
                    profile_label=profile_selector.profile.label)
            except DispenseTimepoint.DoesNotExist:
                DispenseTimepoint.objects.create(
                    schedule=self.schedule,
                    profile_label=profile_selector.profile.label,
                    timepoint=timepoint.timepoint_datetime)


class DispenseScheduleCreator:

    """Creates dispense schedule.
    """

    def __init__(self, schedule=None, schedule_plan=None, subject_identifier=None,
                 sequence=None, arm=None):
        self.schedule = schedule
        self.schedule_plan = schedule_plan
        self.subject_identifier = subject_identifier
        self.sequence = sequence
        self.arm = arm

    def create(self):
        try:
            obj = DispenseSchedule.objects.get(
                subject_identifier=self.subject_identifier,
                name=self.schedule.name,
                start_date=self.schedule.period.start_date.date(),
                end_date=self.schedule.period.end_date.date())
        except DispenseSchedule.DoesNotExist:
            obj = DispenseSchedule.objects.create(
                subject_identifier=self.subject_identifier,
                name=self.schedule.name,
                sequence=self.sequence,
                description=self.schedule.description,
                arm=self.arm,
                start_date=self.schedule.period.start_date.date(),
                end_date=self.schedule.period.end_date.date())
        return obj
