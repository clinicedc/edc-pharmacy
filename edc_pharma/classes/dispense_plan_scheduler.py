from ..classes import ScheduleCollection
from ..plan import dispense_plan
from ..classes import Period
from ..classes import Schedule as SchedulePlan

from ..models import DispenseSchedule, DispenseryPlan


class DispensePlanSchedulerException(Exception):
    pass


class DispensePlanScheduler:

    """Given enrolled subject, calculates the dispense schedules and create
    records for the subject.
    """

    schedule_collection_cls = ScheduleCollection

    def __init__(self, enrolled_subject, *args, **kwargs):
        self.enrolled_subject = enrolled_subject

    @property
    def subject_schedules(self):
        """Returns schedules calculated against a given dispense plan.
        """
        schedules = self.schedule_collection_cls()
        for schedule_name in dispense_plan:
            schedule_details = dispense_plan.get(schedule_name)
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

    def create_dispense_plan(self, **options):
        visits = options.get('plan').visits
        del options['plan']
        for code in visits:
            visit = visits.get(code)
            try:
                DispenseryPlan.objects.get(
                    timepoint=visit.timepoint_datetime,
                    **options)
            except DispenseryPlan.DoesNotExist:
                DispenseryPlan.objects.create(
                    timepoint=visit.timepoint_datetime, **options)

    def prepare(self):
        for seq, schedule_name in enumerate(self.subject_schedules):
            try:
                schedule = self.subject_schedules.get(schedule_name)
                options = {
                    'subject_identifier': self.enrolled_subject.subject_identifier,
                    'plan': schedule}
                obj = DispenseSchedule.objects.get(
                    name=schedule_name,
                    start_date=schedule.period.start_date.date(),
                    end_date=schedule.period.end_date.date())
                options.update({'schedule': obj})
            except DispenseSchedule.DoesNotExist:
                obj = DispenseSchedule.objects.create(
                    name=schedule_name,
                    sequence=seq,
                    start_date=schedule.period.start_date.date(),
                    end_date=schedule.period.end_date.date())
                options.update({'schedule': obj})
            self.create_dispense_plan(**options)
