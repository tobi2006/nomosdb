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

    def test_no_year_entered_in_week_dict_returns_false(self):
        year = self.set_up_year()
        test_day = datetime.date(1955, 10, 11)
        self.assertEqual(week_number(test_day), False)

class AcademicYearStringTest(TestCase):
    """Testing the simple academic year function"""
    
    def test_academic_year_gets_returned_correctly_for_four_digits(self):
        self.assertEqual(
            academic_year_string(1900),
            '1900/01'
        )
    
    def test_academic_year_gets_returned_correctly_for_two_digits(self):
        self.assertEqual(
            academic_year_string(14),
            '14/15'
        )

    def test_academic_year_gets_returned_for_two_digits_in_0_year(self):
        self.assertEqual(
            academic_year_string(00),
            '00/01'
        )
