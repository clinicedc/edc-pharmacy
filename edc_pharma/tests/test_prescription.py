from datetime import datetime

from django.test import TestCase, tag

from ..constants import WEEKS
from ..dispense.dispense_history_creator import DispenseHistoryCreator
from ..models import DispenseAppointment
from ..models import DispenseHistory
from ..print_profile import site_profiles
from ..scheduler import DispenseScheduler


class RandomizedSubjectDummy:

    def __init__(self, randomization_datetime=None, subject_identifier=None):
        self.randomization_datetime = randomization_datetime or datetime.today()
        self.subject_identifier = subject_identifier


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
        dispense = DispenseScheduler(
            randomized_subject=self.randomized_subject,
            dispense_plan=self.dispense_plan,
            arm='control')
        dispense.create_schedules()

    @tag('DispenseCreator')
    def test_dispense_history_creator(self):
        dispense_appointment = DispenseAppointment.objects.filter(
            schedule__subject_identifier=self.randomized_subject.subject_identifier
        ).first()
        creator = DispenseHistoryCreator(
            dispense_appointment=dispense_appointment)
        creator.save_or_update()
        self.assertEqual(DispenseHistory.objects.filter(
            dispense_appointment=dispense_appointment).count(), 2)

    def test_dispense_history_creator_2(self):
        dispense_appointment = DispenseAppointment.objects.filter(
            schedule__subject_identifier=self.randomized_subject.subject_identifier
        ).first()
        creator = DispenseHistoryCreator(
            dispense_appointment=dispense_appointment)
        creator.save_or_update()
        dispense_appointment = DispenseAppointment.objects.filter(
            schedule__subject_identifier=self.randomized_subject.subject_identifier,
            is_dispensed=True
        )
        self.assertEqual(dispense_appointment.count(), 1)

    def test_dispense_history_creator_3(self):
        dispense_appointment = DispenseAppointment.objects.filter(
            schedule__subject_identifier=self.randomized_subject.subject_identifier
        ).order_by('created').first()
        creator = DispenseHistoryCreator(
            dispense_appointment=dispense_appointment)
        creator.save_or_update()
        dispense_appointment = dispense_appointment.next()
        creator = DispenseHistoryCreator(
            dispense_appointment=dispense_appointment)
        creator.save_or_update()
        dispense_appointment = DispenseAppointment.objects.filter(
            schedule__subject_identifier=self.randomized_subject.subject_identifier,
            is_dispensed=True
        )
        self.assertEqual(dispense_appointment.count(), 2)

    def test_dispense_history_creator_selected(self):
        dispense_appointment = DispenseAppointment.objects.filter(
            schedule__subject_identifier=self.randomized_subject.subject_identifier
        ).first()
        creator = DispenseHistoryCreator(
            dispense_appointment=dispense_appointment,
            selected=True,
            medication_name='flucytosine')
        creator.save_or_update()
        history = DispenseHistory.objects.filter(
            dispense_appointment=dispense_appointment)
        self.assertEqual(history.count(), 1)
