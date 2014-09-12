from django.test import TestCase
from main.functions import *
import datetime


class WeekFunctionsTest(TestCase):
    """Testing the functions around the numbers of academic weeks"""

    def set_up_year(self):
        year = Setting.objects.create(name='current_year', value='1900')
        return year

    def test_week_numbers_are_returned_correctly(self):
        year = self.set_up_year()
        test_day = datetime.date(1900, 10, 11)
        self.assertEqual(week_number(test_day), 6)
