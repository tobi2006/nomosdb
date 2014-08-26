from main.models import *
from django.core.exceptions import ValidationError
from django.test import TestCase


def create_subject_area(save=True):
    """Creates one subject area"""
    subject = SubjectArea(name="Law")
    if save:
        subject.save()
    return subject


def create_course(save=True):
    """Creates a course"""
    course = Course(
        title="BA in Cartoon Studies",
        short_title="CS"
    )
    if save:
        course.save()
    return course


def create_student(save=True):
    """Creates a student"""
    student = Student(
        student_id='bb23',
        last_name='Bunny',
        first_name='Bugs Middle Names'
    )
    if save:
        student.save()
    return student


def create_module(save=True):
    """Creates a module"""
    module = Module(
        title='Hunting Laws',
        code="hl23",
        year="2013",
    )
    if save:
        module.save()
    return module


class SubjectAreaTest(TestCase):
    """Tests for the Subject Area class"""

    def test_subject_area_can_be_saved(self):
        subject_in = create_subject_area()
        subject_out = SubjectArea.objects.first()
        self.assertEqual(subject_out.name, 'Law')

    def test_subject_area_returns_name(self):
        subject = create_subject_area(save=False)
        self.assertEqual(
            subject.__str__(),
            "Law"
        )

    def test_subject_area_name_cannot_be_created_twice(self):
        subject1 = create_subject_area()
        subject2 = SubjectArea(name=subject1.name)
        with self.assertRaises(ValidationError):
            subject2.full_clean()


class CourseTest(TestCase):
    """Tests for the Course class"""

    def test_course_can_be_saved(self):
        course_in = create_course()
        course_out = Course.objects.first()
        self.assertEqual(course_out.title, 'BA in Cartoon Studies')
        self.assertEqual(course_out.short_title, 'CS')

    def test_course_returns_name(self):
        course = create_course(save=False)
        self.assertEqual(
            course.__str__(),
            "BA in Cartoon Studies"
        )


class StudentTest(TestCase):
    """Tests for the Student class"""

    def test_student_can_be_saved_to_database_with_basic_attributes(self):
        student_in = create_student()
        student_out = Student.objects.first()
        self.assertEqual(student_out.last_name, 'Bunny')
        self.assertEqual(student_out.first_name, 'Bugs Middle Names')
        self.assertEqual(student_out.student_id, 'bb23')
        self.assertEqual(student_out.nalp, False)
        self.assertEqual(student_out.active, True)
        self.assertEqual(student_out.qld, True)

    def test_student_without_student_id_cannot_be_saved(self):
        student = Student(last_name="Bunny")
        with self.assertRaises(ValidationError):
            student.save()
            student.full_clean()

    def test_student_with_existing_student_id_cannot_be_saved(self):
        create_student()
        with self.assertRaises(ValidationError):
            student_2 = Student(
                student_id="bb23",
                last_name="Buffins"
            )
            student_2.full_clean()

    def test_student_name_returns_correctly(self):
        student = create_student(save=False)
        self.assertEqual(
            student.__str__(),
            'Bunny, Bugs Middle Names'
        )

    def test_student_returns_correct_url(self):
        student = create_student(save=False)
        self.assertEqual(student.get_absolute_url(), '/student/bb23/')

    def test_edit_student_returns_correct_url(self):
        student = create_student(save=False)
        self.assertEqual(student.get_edit_url(), '/edit_student/bb23/')

    def test_student_can_be_enlisted_in_module(self):
        student = create_student()
        module = Module.objects.create(code="hl23", year="2013")
        student.modules.add(module)
        student.save()
        self.assertEqual(student, module.student_set.first())

    def test_student_short_names_return_correctly(self):
        student = create_student(save=False)
        self.assertEqual(student.short_name(), 'Bunny, Bugs')
        self.assertEqual(student.short_first_name(), 'Bugs')


class AssessmentTest(TestCase):
    """Tests for the Assessment class"""

    def test_assessment_can_be_saved_and_slug_gets_created(self):
        assessment_in = Assessment.objects.create(
            title="Practical Hunting Exercise",
            value=40
        )
        assessment_out = Assessment.objects.first()
        self.assertEqual(assessment_out.title, 'Practical Hunting Exercise')
        self.assertEqual(assessment_out.value, 40)
        self.assertEqual(assessment_out.slug, 'practical-hunting-exercise')

    def test_assessment_returns_correct_url(self):
        module = create_module()
        assessment = Assessment.objects.create(
            title="Practical Hunting Exercise",
            value=40
        )
        module.assessments.add(assessment)
        self.assertEqual(
            assessment.get_absolute_url(),
            '/edit_assessment/hl23/2013/practical-hunting-exercise/'
        )

    def test_assessment_returns_correct_delete_url(self):
        module = create_module()
        assessment = Assessment.objects.create(
            title="Practical Hunting Exercise",
            value=40,
            module=module
        )
        self.assertEqual(
            assessment.get_delete_url(),
            '/delete_assessment/hl23/2013/practical-hunting-exercise/'
        )


class ModuleTest(TestCase):
    """Tests for the Module class"""

    def test_module_can_be_saved_to_database_with_basic_attributes(self):
        module_in = create_module()
        module_out = Module.objects.first()
        self.assertEqual(module_out.title, "Hunting Laws")
        self.assertEqual(module_out.code, "hl23")
        self.assertEqual(module_out.year, 2013)

    def test_module_name_returns_correctly(self):
        module = create_module(save=False)
        self.assertEqual(
            module.__str__(),
            'Hunting Laws (2013/14)'
        )

    def test_module_returns_correct_url(self):
        module = create_module(save=False)
        self.assertEqual(
            module.get_absolute_url(),
            '/module/hl23/2013/'
        )

    def test_second_module_with_identical_code_and_year_cannot_be_saved(self):
        module1 = create_module()
        module2 = Module(
            title="A different title",
            code="hl23",
            year="2013"
        )
        with self.assertRaises(ValidationError):
            module2.full_clean()

    def test_module_returns_correct_add_students_url(self):
        module = create_module(save=False)
        self.assertEqual(
            module.get_add_students_url(),
            '/add_students_to_module/hl23/2013/')

    def test_module_returns_correct_attendance_url(self):
        module = create_module(save=False)
        self.assertEqual(
            module.get_attendance_url('all'),
            '/attendance/hl23/2013/all/'
        )
        self.assertEqual(
            module.get_attendance_url(1),
            '/attendance/hl23/2013/1/'
        )

    def test_module_returns_blank_remove_students_url(self):
        module = create_module(save=False)
        self.assertEqual(
            module.get_blank_remove_student_url(),
            '/remove_student_from_module/hl23/2013/'
        )

    def test_module_returns_correct_assessment_url(self):
        module = create_module(save=False)
        self.assertEqual(
            module.get_assessment_url(),
            '/assessment/hl23/2013/'
        )

    def test_module_returns_all_assessment_titles_in_list(self):
        module1 = create_module()
        m_1_assessment_1 = Assessment.objects.create(
            title='Practical Exercise',
            value=40
        )
        module1.assessments.add(m_1_assessment_1)
        m_1_assessment_2 = Assessment.objects.create(
            title='Exam',
            value=60
        )
        module1.assessments.add(m_1_assessment_2)
        module2 = Module.objects.create(
            title="A different title",
            code="DT42",
            year="2013",
        )
        m_2_assessment_1 = Assessment.objects.create(
            title="Assessment 1",
            value=20
        )
        module2.assessments.add(m_2_assessment_1)
        m_2_assessment_2 = Assessment.objects.create(
            title="Assessment 2",
            value=20,
        )
        module2.assessments.add(m_2_assessment_2)
        m_2_assessment_3 = Assessment.objects.create(
            title="Assessment 3",
            value=60,
        )
        module2.assessments.add(m_2_assessment_3)
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

    def test_module_returns_all_week_numbers_correctly(self):
        module = create_module(save=False)
        module.first_session = 5
        module.last_session = 17
        module.no_teaching_in = '6,12'
        sessions = [5, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17]
        self.assertEqual(module.all_teaching_weeks(), sessions)


class PerformanceTest(TestCase):
    """Tests for the Performance class"""

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
        student = create_student()
        # First module with all marks
        module = create_module()
        performance1 = Performance.objects.create(
            module=module,
            student=student
        )
        assessment = Assessment.objects.create(
            title="Assessment 1",
            value=20
        )
        module.assessments.add(assessment)
        result = AssessmentResult.objects.create(
            assessment=assessment,
            part_of=performance1,
            mark=20
        )
        assessment = Assessment.objects.create(
            title="Assessment 2",
            value=20
        )
        module.assessments.add(assessment)
        result = AssessmentResult.objects.create(
            assessment=assessment,
            part_of=performance1,
            mark=30
        )
        assessment = Assessment.objects.create(
            title="Assessment 3",
            value=20,
        )
        module.assessments.add(assessment)
        result = AssessmentResult.objects.create(
            assessment=assessment,
            part_of=performance1,
            mark=40
        )
        assessment = Assessment.objects.create(
            title="Exam",
            value=40
        )
        module.assessments.add(assessment)
        # No result for the exam - should return "None"
        expected_list_1 = ['20', '30', '40', None]

        module2 = Module.objects.create(
            title="And another one",
            code="AAO4223"
        )
        performance2 = Performance.objects.create(
            module=module2,
            student=student
        )
        assessment = Assessment.objects.create(
            title="Zo far back in the alphabet",
            value=30
        )
        module2.assessments.add(assessment)
        result = AssessmentResult.objects.create(
            assessment=assessment,
            part_of=performance2,
            mark=50
        )
        assessment = Assessment.objects.create(
            title="And another assessment",
            value=10
        )
        module2.assessments.add(assessment)
        result = AssessmentResult.objects.create(
            assessment=assessment,
            part_of=performance2,
            mark=35,
            resit_mark=38,
            concessions='G',
            second_resit_mark=40
        )
        assessment = Assessment.objects.create(
            title="Middle Assessment",
            value=10
        )
        module2.assessments.add(assessment)
        expected_list_2 = [
            '35 (Submission: 38, Second resubmission: 40)',
            None,
            '50'
        ]
        self.assertEqual(
            performance1.all_assessment_results_as_strings(),
            expected_list_1
        )
        self.assertEqual(
            performance2.all_assessment_results_as_strings(),
            expected_list_2
        )

    def test_attendance_can_be_saved_and_checked(self):
        module = create_module()
        student = create_student()
        performance = Performance.objects.create(
            module=module,
            student=student
        )
        performance.save_attendance(1, 'p')
        performance.save_attendance('2', 'a')
        performance.save_attendance('3', 'e')
        performance.save_attendance(5, 'p')
        performance.save_attendance(6, 'p')
        performance.save_attendance(7, 'p')
        performance.save_attendance(8, 'p')
        performance.save_attendance(9, 'a')
        performance.save_attendance('10', 'a')
        self.assertEqual(performance.attendance_for('6'), 'p')
        self.assertEqual(performance.attendance_for('4'), None)
        self.assertEqual(performance.attendance_for(9), 'a')
        self.assertEqual(performance.attendance_for(10), 'a')
        self.assertEqual(performance.count_attendance(), '6/9')
        performance.save_attendance(11, 'a')
        self.assertEqual(performance.count_attendance(), '6/10')
        self.assertEqual(
            performance.attendance_as_list(),
            ['p', 'a', 'e', 'p', 'p', 'p', 'p', 'a', 'a', 'a']
        )
        self.assertTrue(performance.missed_the_last_two_sessions())
