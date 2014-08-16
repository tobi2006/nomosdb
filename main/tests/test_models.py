from main.models import Student, Module, SubjectArea, Course, Performance
from django.core.exceptions import ValidationError
from django.test import TestCase


def create_subject_area(save=True):
    subject = SubjectArea(name="Alchemy")
    if save:
        subject.save()
    return subject


def create_course(save=True):
    course = Course(
        title="BA in Wizard Studies",
        short_title="WS"
    )
    if save:
        course.save()
    return course


def create_student(save=True):
    student = Student(
        student_id='FB4223',
        last_name='Baggins',
        first_name='Frodo Middle Names'
    )
    if save:
        student.save()
    return student


def create_module(save=True):
    module = Module(
        title="Module Title",
        code="MT23",
        year="2013",
    )
    if save:
        module.save()
    return module


class SubjectAreaTest(TestCase):

    def test_subject_area_can_be_saved(self):
        subject_in = create_subject_area()
        subject_out = SubjectArea.objects.first()
        self.assertEqual(subject_out.name, 'Alchemy')

    def test_subject_area_returns_name(self):
        subject = create_subject_area(save=False)
        self.assertEqual(
            subject.__unicode__(),
            "Alchemy"
        )

    def test_subject_area_name_cannot_be_created_twice(self):
        subject1 = create_subject_area()
        subject2 = SubjectArea(name=subject1.name)
        with self.assertRaises(ValidationError):
            subject2.full_clean()


class CourseTest(TestCase):

    def test_course_can_be_saved(self):
        course_in = create_course()
        course_out = Course.objects.first()
        self.assertEqual(course_out.title, 'BA in Wizard Studies')
        self.assertEqual(course_out.short_title, 'WS')

    def test_course_returns_name(self):
        course = create_course(save=False)
        self.assertEqual(
            course.__unicode__(),
            "BA in Wizard Studies"
        )


class StudentTest(TestCase):

    def test_student_can_be_saved_to_database_with_basic_attributes(self):
        student_in = create_student()
        student_out = Student.objects.first()
        self.assertEqual(student_out.last_name, 'Baggins')
        self.assertEqual(student_out.first_name, 'Frodo Middle Names')
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
        create_student()
        with self.assertRaises(ValidationError):
            student_2 = Student(
                student_id="FB4223",
                last_name="Buffins"
            )
            student_2.full_clean()

    def test_student_name_returns_correctly(self):
        student = create_student(save=False)
        self.assertEqual(
            student.__unicode__(),
            'Baggins, Frodo Middle Names'
        )

    def test_student_returns_correct_url(self):
        student = create_student(save=False)
        self.assertEqual(student.get_absolute_url(), '/student/FB4223/')

    def test_edit_student_returns_correct_url(self):
        student = create_student(save=False)
        self.assertEqual(student.get_edit_url(), '/edit_student/FB4223/')

    def test_student_can_be_enlisted_in_module(self):
        student = create_student()
        module = Module.objects.create(code="MT23", year="2013")
        student.modules.add(module)
        student.save()
        self.assertEqual(student, module.student_set.first())

    def test_student_short_names_return_correctly(self):
        student = create_student(save=False)
        self.assertEqual(student.short_name(), 'Baggins, Frodo')
        self.assertEqual(student.short_first_name(), 'Frodo')


class ModuleTest(TestCase):

    def test_module_can_be_saved_to_database_with_basic_attributes(self):
        module_in = create_module()
        module_out = Module.objects.first()
        self.assertEqual(module_out.title, "Module Title")
        self.assertEqual(module_out.code, "MT23")
        self.assertEqual(module_out.year, 2013)

    def test_module_name_returns_correctly(self):
        module = create_module(save=False)
        self.assertEqual(
            module.__unicode__(),
            'Module Title (2013/14)'
        )

    def test_module_returns_correct_url(self):
        module = create_module(save=False)
        self.assertEqual(
            module.get_absolute_url(),
            '/module/MT23/2013/'
        )

    def test_second_module_with_identical_code_and_year_cannot_be_saved(self):
        module1 = create_module()
        module2 = Module(
            title="A different title",
            code="MT23",
            year="2013"
        )
        with self.assertRaises(ValidationError):
            module2.full_clean()

    def test_module_returns_correct_add_students_url(self):
        module = create_module(save=False)
        self.assertEqual(
            module.get_add_students_url(),
            '/add_students_to_module/MT23/2013/')

    def test_module_returns_all_assessment_titles_in_list(self):
        module1 = create_module(save=False)
        module1.assessment_1_title = "Practical Exercise"
        module1.assessment_1_value = 40
        module1.exam_value = 60
        module2 = Module(
            title="A different title",
            code="MT23",
            year="2013",
            assessment_1_title="Assessment 1",
            assessment_1_value=20,
            assessment_2_title="Assessment 2",
            assessment_2_value=20,
            assessment_3_title="Assessment 3",
            assessment_3_value=60,
            exam_value=0
        )
        list_of_assessments_1 = [
            ("Practical Exercise", 40),
            ("Exam", 60)
        ]
        list_of_assessments_2 = [
            ("Assessment 1", 20),
            ("Assessment 2", 20),
            ("Assessment 3", 60)
        ]
        self.assertEqual(
            module1.all_assessment_titles(), list_of_assessments_1)
        self.assertEqual(
            module2.all_assessment_titles(), list_of_assessments_2)


class PerformanceTest(TestCase):

    def test_enlisting_a_student_in_a_module_creates_performance_item(self):
        student = create_student()
        module = create_module()
        response = self.client.post(
            '/add_students_to_module/%s/%s/' % (module.code, module.year),
            data={'student_ids': [student.student_id, ]}
        )
        performance = Performance.objects.first()
        self.assertEqual(performance.module, module)
        self.assertEqual(performance.student, student)

    def test_performance_returns_all_assessment_results(self):
        module = Module.objects.create(
            title="A module title",
            code="MT23",
            year=2013,
            assessment_1_title="Assessment 1",
            assessment_1_value=20,
            assessment_2_title="Assessment 2",
            assessment_2_value=20,
            assessment_3_title="Assessment 3",
            assessment_3_value=20,
            exam_value=40
        )
        module2 = Module.objects.create(
            title="Another Module",
            year=2013,
            code="AM42",
            assessment_1_title="Assessment 1",
            assessment_1_value=30,
            assessment_2_title="Assessment 2",
            assessment_2_value=20,
            assessment_3_title="Assessment 3",
            assessment_3_value=50,
            exam_value=0
        )
        module3 = Module.objects.create(
            title="Yet Another Module",
            year=2013,
            code="YAM42",
            assessment_1_title="Assessment 1",
            assessment_1_value=20,
            assessment_2_title="Assessment 2",
            assessment_2_value=20,
            assessment_3_title="Assessment 3",
            assessment_3_value=10,
            assessment_4_title="Assessment 4",
            assessment_4_value=10,
            assessment_5_title="Assessment 5",
            assessment_5_value=10,
            assessment_6_title="Assessment 6",
            assessment_6_value=10,
            exam_value=20
        )
        student = create_student()
        performance1 = Performance(
            module=module,
            student=student,
            assessment_1=20,
            assessment_2=30,
            assessment_3=40,
            assessment_4=50,
            exam=60
        )
        expected_list_1 = ['20', '30', '40', '60']
        performance2 = Performance(
            module=module2,
            student=student,
            assessment_1=0,
            r_assessment_1=50,
            assessment_1_concessions='G',
            assessment_2=40,
            assessment_3=20,
            assessment_3_concessions='N',
            r_assessment_3=30,
            s_assessment_3=40
        )
        expected_list_2 = [
            '0 (Submission: 50)',
            '40',
            '20 (Resubmission: 30, Second resubmission: 40)'
        ]
        performance3 = Performance(
            module=module3,
            student=student,
            assessment_1=40,
            assessment_2=40,
            assessment_3=40,
            assessment_4=40,
            assessment_5=30,
            assessment_5_concessions='G',
            r_assessment_5=40,
            assessment_6=35,
            assessment_6_concessions='N',
            r_assessment_6=37,
            s_assessment_6=40,
            exam=35,
            exam_concessions='G',
            r_exam=37,
            s_exam=40
        )
        expected_list_3 = [
            '40',
            '40',
            '40',
            '40',
            '30 (Submission: 40)',
            '35 (Resubmission: 37, Second resubmission: 40)',
            '35 (Sit: 37, Second resit: 40)'
        ]
        self.assertEqual(performance1.assessment_result_as_string(1), '20')
        self.assertEqual(
            performance1.all_assessment_results_as_strings(),
            expected_list_1
        )
        self.assertEqual(
            performance2.all_assessment_results_as_strings(),
            expected_list_2
        )
        self.assertEqual(
            performance3.all_assessment_results_as_strings(),
            expected_list_3
        )
