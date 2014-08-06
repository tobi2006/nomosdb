from database.models import Student
from django.core.exceptions import ValidationError
from django.test import TestCase


class StudentTest(TestCase):

    def test_student_can_be_saved_to_database_with_basic_attributes(self):
        student_in = Student()
        student_in.student_id = 'FB4223'
        student_in.last_name = 'Baggins'
        student_in.first_name = 'Frodo'
        student_in.save()
        student_out = Student.objects.first()
        self.assertEqual(student_out.last_name, 'Baggins')
        self.assertEqual(student_out.first_name, 'Frodo')
        self.assertEqual(student_out.student_id, 'FB4223')
        self.assertEqual(student_out.nalp, False)
        self.assertEqual(student_out.active, True)
        self.assertEqual(student_out.qld, True)

    def test_student_without_student_id_cannot_be_saved(self):
        student = Student(last_name="Baggins")
        with self.assertRaises(ValidationError):
            student.save()
            student.full_clean()

    def test_student_with_existing_student_id_cannot_be_saved(self):
        student_1 = Student.objects.create(
            student_id="FB4223",
            last_name="Baggins"
        )
        with self.assertRaises(ValidationError):
            student_2 = Student(
                student_id="FB4223",
                last_name="Buffins"
            )
            student_2.full_clean()

    def test_student_returns_correct_url(self):
        student = Student.objects.create(student_id="FB4223")
        self.assertEqual(student.get_absolute_url(), '/student/FB4223/')
    
    def test_edit_student_returns_correct_url(self):
        student = Student.objects.create(student_id="FB4223")
        self.assertEqual(student.get_edit_url(), '/edit_student/FB4223/')
