from django.test import TestCase
from main.forms import *

class StudentFormTest(TestCase):

    def test_student_form_contains_right_form_elements(self):
        form = StudentForm()
        self.assertIn('id="id_last_name"', form.as_p())
        self.assertIn('id="id_first_name"', form.as_p())
        self.assertIn('id="id_student_id"', form.as_p())

    def test_student_form_validates_that_student_id_is_included(self):
        form = StudentForm(data={'student_id': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['student_id'], [NO_STUDENT_ID_ERROR])

    def test_student_form_validates_unique_id(self):
        Student.objects.create(
            last_name="Baggins",
            first_name="Frodo",
            student_id="FB2342"
        )
        form1 = StudentForm(data={
            'last_name': "Boffins",
            'first_name': "Frildo",
            'student_id': "FB2342"
        })
        form2 = StudentForm(data={
            'last_name': "Boffins",
            'first_name': "Frildo",
            'student_id': "FB2343"
        })
        self.assertFalse(form1.is_valid())
        self.assertTrue(form2.is_valid())


class ModuleFormTest(TestCase):

    def test_module_form_contains_right_form_elements(self):
        form = ModuleForm()
        self.assertIn('id="id_title"', form.as_p())
        self.assertIn('id="id_code"', form.as_p())
        self.assertIn('id="id_year"', form.as_p())


class StaffFormTest(TestCase):

    def test_staff_form_contains_right_elements(self):
        form = StaffForm()
        self.assertIn('id="id_first_name"', form.as_p())
        self.assertIn('id="id_last_name"', form.as_p())
        self.assertIn('id="id_email"', form.as_p())
        self.assertIn('id="id_subject_areas"', form.as_p())
