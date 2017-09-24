from datetime import datetime

from django.test import TestCase

from ..classes.move_day import MoveDayError, MoveDay


class TestMoveDay(TestCase):

    def test_move_day_forward(self):
        day = datetime(2017, 9, 30)
        move = MoveDay(day=day, forward=True)
        self.assertNotEqual(move.day, datetime(2017, 9, 30).date())

    def test_move_day_backward(self):
        day = datetime(2017, 9, 30)
        move = MoveDay(day=day, backward=True)
        self.assertNotEqual(move.day, datetime(2017, 9, 30).date())

    def test_move_both_error(self):
        day = datetime(2017, 9, 30)
        self.assertRaises(
            MoveDayError, MoveDay, day=day, forward=True, backward=True)

    def test_move_both_error1(self):
        self.assertRaises(MoveDayError, MoveDay, day=None)
