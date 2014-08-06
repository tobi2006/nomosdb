from django.test import TestCase
from database.forms import *

class StudentFormTest(TestCase):

    def test_student_form_contains_right_form_elements(self):
        form = StudentForm()
        self.assertIn('id="id_last_name"', form.as_p())
        self.assertIn('id="id_first_name"', form.as_p())
        self.assertIn('id="id_student_id"', form.as_p())

    def test_student_form_validates_unique_student_id(self):
        form = StudentForm(data={'student_id': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['student_id'], [NO_STUDENT_ID_ERROR])
