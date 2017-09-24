from ..classes import ScheduleCollection
from ..plan import dispense_plan
from ..classes import Period
from ..classes import Schedule as SchedulePlan

from ..models import DispenseSchedule, DispenseryPlan


class DispensePlanSchedulerException(Exception):
    pass


class DispensePlanScheduler:

    schedule_collection = ScheduleCollection

    def __init__(self, enrolled_subject, *args, **kwargs):
        self.enrolled_subject = enrolled_subject

    @property
    def subject_schedules(self):
        collection = self.schedule_collection()
        for name in dispense_plan:
            schedule_details = dispense_plan.get(name)
            period = Period(
                timepoint=collection.next_timepoint or self.enrolled_subject.report_datetime,
                weeks=schedule_details.get('duration'),)
            schedule = SchedulePlan(
                name=name,
                number_of_visits=schedule_details.get('number_of_visits'),
                period=period)
            collection.add(schedule=schedule)
        return collection

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
