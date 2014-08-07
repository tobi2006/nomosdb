from main.models import Student, Module, SubjectArea
from django.core.exceptions import ValidationError
from django.test import TestCase


class SubjectAreaTest(TestCase):

    def test_subject_area_can_be_saved(self):
        subject_in = SubjectArea.objects.create(
            title="Alchemy",
            short_title="Alc"
        )
        subject_out = SubjectArea.objects.first()
        self.assertEqual(subject_out.title, 'Alchemy')
        self.assertEqual(subject_out.short_title, 'Alc')

    def test_subject_area_returns_title(self):
        subject = SubjectArea(
            title="Alchemy",
            short_title="Alc"
        )
        self.assertEqual(
            subject.__unicode__(),
            "Alchemy"
        )


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

    def test_student_name_returns_correctly(self):
        student = Student(
            student_id="FB4223",
            last_name="Baggins",
            first_name="Frodo Middle Names"
        )
        self.assertEqual(
            student.__unicode__(),
            'Baggins, Frodo Middle Names'
        )
            

    def test_student_returns_correct_url(self):
        student = Student.objects.create(student_id="FB4223")
        self.assertEqual(student.get_absolute_url(), '/student/FB4223/')
    
    def test_edit_student_returns_correct_url(self):
        student = Student.objects.create(student_id="FB4223")
        self.assertEqual(student.get_edit_url(), '/edit_student/FB4223/')


class ModuleTest(TestCase):

    def set_up_test_module(self, save=True):
        module = Module(
            title="Module Title",
            code="MT23",
            year="2013",
        )
        if save:
            module.save()
        return module

    def test_module_can_be_saved_to_database_with_basic_attributes(self):
        module_in = self.set_up_test_module()
        module_out = Module.objects.first()
        self.assertEqual(module_out.title, "Module Title")
        self.assertEqual(module_out.code, "MT23")
        self.assertEqual(module_out.year, 2013)

    def test_module_name_returns_correctly(self):
        module = self.set_up_test_module(save=False)
        self.assertEqual(
            module.__unicode__(),
            'Module Title (2013/14)'
        )

    def test_module_returns_correct_url(self):
        module = self.set_up_test_module(save=False)
        self.assertEqual(
            module.get_absolute_url(),
            '/module/MT23/2013/'
        )

    def test_second_module_with_identical_code_and_year_cannot_be_saved(self):
        module1 = self.set_up_test_module()
        module2 = Module(
            title="A different title",
            code="MT23",
            year="2013"
        )
        with self.assertRaises(ValidationError):
            module2.full_clean()
