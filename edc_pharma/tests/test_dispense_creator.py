from datetime import datetime
from edc_pharma.dispense.dispense_history_creator import DispenseHistoryCreator
from edc_pharma.models.dispense_history import DispenseHistory
from edc_pharma.models.dispense_timepoint import DispenseTimepoint

from django.test import tag, TestCase

from ..constants import WEEKS
from ..print_profile import site_profiles
from ..scheduler import DispensePlanScheduler


class RandomizedSubjectDummy:

    def __init__(self, randomization_datetime=None, subject_identifier=None):
        self.randomization_datetime = randomization_datetime or datetime.today()
        self.subject_identifier = subject_identifier


@tag('TestDispenseCreator')
class TestDispenseCreator(TestCase):

    def setUp(self):
        self.dispense_plan = {
            'schedule1': {
                'number_of_visits': 2, 'duration': 2, 'unit': WEEKS,
                'dispense_profile': {
                    'enrollment': site_profiles.get(name='enrollment.control'),
                    'followup': site_profiles.get(name='followup.control'),
                }},
            'schedule2': {
                'number_of_visits': 2, 'duration': 8, 'unit': WEEKS,
                'dispense_profile': {
                    'enrollment': site_profiles.get(name='enrollment.control'),
                    'followup': site_profiles.get(name='followup.control'),
                }}}
        self.randomized_subject = RandomizedSubjectDummy(
            randomization_datetime=datetime(2017, 8, 24),
            subject_identifier='1111')
        dispense = DispensePlanScheduler(
            randomized_subject=self.randomized_subject,
            dispense_plan=self.dispense_plan,
            arm='control')
        dispense.create_schedules()

    def test_dispense_history_creator(self):
        dispense_timepoint = DispenseTimepoint.objects.filter(
            schedule__subject_identifier=self.randomized_subject.subject_identifier
        ).first()
        creator = DispenseHistoryCreator(
            dispense_timepoint=dispense_timepoint)
        creator.save_or_update()

        self.assertEqual(DispenseHistory.objects.filter(
            dispense_timepoint=dispense_timepoint).count(), 1)

    def test_dispense_history_creator_1(self):
        dispense_timepoint = DispenseTimepoint.objects.filter(
            schedule__subject_identifier=self.randomized_subject.subject_identifier
        ).first()
        creator = DispenseHistoryCreator(
            dispense_timepoint=dispense_timepoint)
        creator.save_or_update()
        dispensed_medications = DispenseHistory.objects.get(
            dispense_timepoint=dispense_timepoint)
        self.assertEqual(dispensed_medications.medications.all().count(), 2)

    def test_dispense_history_creator_2(self):
        dispense_timepoint = DispenseTimepoint.objects.filter(
            schedule__subject_identifier=self.randomized_subject.subject_identifier
        ).first()
        creator = DispenseHistoryCreator(
            dispense_timepoint=dispense_timepoint)
        creator.save_or_update()
        dispense_timepoint = DispenseTimepoint.objects.filter(
            schedule__subject_identifier=self.randomized_subject.subject_identifier,
            is_dispensed=True
        )
        self.assertEqual(dispense_timepoint.count(), 1)

    @tag('creator_3')
    def test_dispense_history_creator_3(self):
        dispense_timepoint = DispenseTimepoint.objects.filter(
            schedule__subject_identifier=self.randomized_subject.subject_identifier
        ).order_by('created').first()
        creator = DispenseHistoryCreator(
            dispense_timepoint=dispense_timepoint)
        creator.save_or_update()
        dispense_timepoint = dispense_timepoint.next()
        creator = DispenseHistoryCreator(
            dispense_timepoint=dispense_timepoint)
        creator.save_or_update()
        dispense_timepoint = DispenseTimepoint.objects.filter(
            schedule__subject_identifier=self.randomized_subject.subject_identifier,
            is_dispensed=True
        )
        self.assertEqual(dispense_timepoint.count(), 2)
