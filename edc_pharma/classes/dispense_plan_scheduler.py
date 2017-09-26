from ..classes import Period
from ..classes import Schedule as SchedulePlan
from ..classes import ScheduleCollection

from .creators import DispenseScheduleCreator, DispenseTimepointCreator


class DispensePlanSchedulerException(Exception):
    pass


class InvalidSchedulePlanConfig(Exception):
    pass


class DispensePlanScheduler:

    """Given enrolled subject, calculates the dispense schedules and create
    records for the subject.
    """

    schedule_collection_cls = ScheduleCollection
    dispense_timepoint_cls = DispenseTimepointCreator
    dispense_schedule_creator_cls = DispenseScheduleCreator

    def __init__(self, enrolled_subject, dispense_plan=None, profile_selector=None,
                 *args, **kwargs):
        self.enrolled_subject = enrolled_subject
        self.dispense_plan = dispense_plan
        self.profile_selector = profile_selector

    @property
    def subject_schedules(self):
        """Returns schedules calculated against a given dispense plan.
        """
        schedules = self.schedule_collection_cls()
        for schedule_name in self.dispense_plan or {}:
            self.validate_dispense_plan(dispense_plan=self.dispense_plan)
            schedule_details = self.dispense_plan.get(schedule_name)
            schedule_period = Period(
                timepoint=schedules.next_timepoint or self.enrolled_subject.report_datetime,
                duration=schedule_details.get('duration'),
                unit=schedule_details.get('unit'))
            schedule = SchedulePlan(
                name=schedule_name,
                number_of_visits=schedule_details.get('number_of_visits'),
                period=schedule_period)
            schedules.add(schedule=schedule)
        return schedules

    def validate_dispense_plan(self, dispense_plan):
        for item in dispense_plan or {}:
            try:
                plan = dispense_plan.get(item)
                plan['unit']
                plan['duration']
                plan['number_of_visits']
                plan['dispense_profile']
            except KeyError as e:
                raise InvalidSchedulePlanConfig(f'Missing expected key {e}')

    def prepare(self):
        for sequence, schedule_name in enumerate(self.subject_schedules):
            sequence = sequence + 1
            schedule = self.subject_schedules.get(schedule_name)
            schedule_obj = self.dispense_schedule_creator_cls(
                schedule=schedule,
                subject_identifier=self.enrolled_subject.subject_identifier,
                sequence=sequence).create()
            schedule_plan = self.dispense_plan.get(schedule_name)

            self.dispense_timepoint_cls(
                schedule_name=schedule_name, schedule_plan=schedule_plan,
                schedule=schedule_obj,
                timepoints=schedule.visits,
            ).create()
