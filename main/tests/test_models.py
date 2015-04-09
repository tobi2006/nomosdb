from feedback.models import IndividualFeedback
from main.models import *
from main.views import *
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from .base import *


class SubjectAreaTest(AdminUnitTest):
    """Tests for the Subject Area class"""

    def test_subject_area_can_be_saved(self):
        subject_in = create_subject_area()
        subject_out = SubjectArea.objects.first()
        self.assertEqual(subject_out.name, 'Cartoon Studies')

    def test_subject_area_returns_name(self):
        subject = create_subject_area(save=False)
        self.assertEqual(
            subject.__str__(),
            "Cartoon Studies"
        )

    def test_subject_area_name_cannot_be_created_twice(self):
        subject1 = create_subject_area()
        subject2 = SubjectArea(name=subject1.name)
        with self.assertRaises(ValidationError):
            subject2.full_clean()


class CourseTest(AdminUnitTest):
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


class StudentTest(TeacherUnitTest):
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
        module = Module.objects.create(code="hl23", year="1900")
        student.modules.add(module)
        student.save()
        self.assertEqual(student, module.students.first())

    def test_student_short_names_return_correctly(self):
        student = create_student(save=False)
        self.assertEqual(student.short_name(), 'Bunny, Bugs')
        self.assertEqual(student.short_first_name(), 'Bugs')

    def test_student_and_all_performances_can_be_deleted(self):
        student = create_student()
        module = create_module()
        performance = Performance.objects.create(
            student=student, module=module)
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(Performance.objects.count(), 1)
        student.delete()
        self.assertEqual(Student.objects.count(), 0)
        self.assertEqual(Performance.objects.count(), 0)


class StaffTest(AdminUnitTest):
    """Tests for the Staff class"""

    def test_staff_member_can_be_created(self):
        user = create_user()
        teacher = Staff.objects.create(
            user=user,
            role='teacher'
        )
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(Staff.objects.count(), 2)
        staff_out = Staff.objects.get(role="teacher")
        self.assertEqual(staff_out.user.last_name, 'Fudd')

    def test_staff_member_returns_correct_edit_url(self):
        staff = create_teacher(save=False)
        self.assertEqual(staff.get_edit_url(), '/edit_staff/ef123/')


class AssessmentTest(TeacherUnitTest):
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
            '/edit_assessment/hl23/1900/practical-hunting-exercise/'
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
            '/delete_assessment/hl23/1900/practical-hunting-exercise/'
        )

    def test_assessment_returns_correct_mark_all_url(self):
        module = create_module()
        assessment = Assessment.objects.create(
            title='Practical Hunting Exercise',
            value=100,
            module=module
        )
        self.assertEqual(
            assessment.get_mark_all_url(),
            '/mark_all/hl23/1900/practical-hunting-exercise/first/'
        )

    def test_assessment_returns_correct_mark_all_anonymously_url(self):
        module = create_module()
        assessment = Assessment.objects.create(
            title='Practical Hunting Exercise',
            value=100,
            module=module
        )
        self.assertEqual(
            assessment.get_mark_all_url(anonymous=True),
            '/mark_all_anonymously/hl23/1900/practical-hunting-exercise/first/'
        )


class ModuleTest(TeacherUnitTest):
    """Tests for the Module class"""

    def test_module_can_be_saved_to_database_with_basic_attributes(self):
        module_in = create_module()
        module_out = Module.objects.first()
        self.assertEqual(module_out.title, "Hunting Laws")
        self.assertEqual(module_out.code, "hl23")
        self.assertEqual(module_out.year, 1900)

    def test_module_name_returns_correctly(self):
        module = create_module(save=False)
        self.assertEqual(
            module.__str__(),
            'Hunting Laws (1900/01)'
        )

    def test_module_returns_correct_url(self):
        module = create_module(save=False)
        self.assertEqual(
            module.get_absolute_url(),
            '/module/hl23/1900/'
        )

    def test_second_module_with_identical_code_and_year_cannot_be_saved(self):
        module1 = create_module()
        module2 = Module(
            title="A different title",
            code="hl23",
            year="1900"
        )
        with self.assertRaises(ValidationError):
            module2.full_clean()

    def test_module_returns_correct_add_students_url(self):
        module = create_module(save=False)
        self.assertEqual(
            module.get_add_students_url(),
            '/add_students_to_module/hl23/1900/')

    def test_module_returns_correct_attendance_url(self):
        module = create_module(save=False)
        self.assertEqual(
            module.get_attendance_url('all'),
            '/attendance/hl23/1900/all/'
        )
        self.assertEqual(
            module.get_attendance_url(1),
            '/attendance/hl23/1900/1/'
        )

    def test_module_returns_blank_remove_students_url(self):
        module = create_module(save=False)
        self.assertEqual(
            module.get_blank_remove_student_url(),
            '/remove_student_from_module/hl23/1900/'
        )

    def test_module_returns_correct_assessment_url(self):
        module = create_module(save=False)
        self.assertEqual(
            module.get_assessment_url(),
            '/assessment/hl23/1900/'
        )

    def test_module_returns_all_assessment_titles_in_list(self):
        module1 = create_module()
        m_1_assessment_1 = Assessment.objects.create(
            title='Practical Exercise',
            value=40,
            available=True
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
            year="1900",
        )
        m_2_assessment_1 = Assessment.objects.create(
            title="Assessment 1",
            value=20
        )
        module2.assessments.add(m_2_assessment_1)
        m_2_assessment_2 = Assessment.objects.create(
            title="Assessment 2",
            value=20,
            available=True
        )
        module2.assessments.add(m_2_assessment_2)
        m_2_assessment_3 = Assessment.objects.create(
            title="Assessment 3",
            value=60,
        )
        module2.assessments.add(m_2_assessment_3)
        list_of_assessments_1 = [
            ("Practical Exercise", 40, True),
            ("Exam", 60, False)
        ]
        list_of_assessments_2 = [
            ("Assessment 1", 20, False),
            ("Assessment 2", 20, True),
            ("Assessment 3", 60, False)
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

    def test_module_all_nine_averages_returns_all_averages_with_9_at_end(self):
        stuff = set_up_stuff()
        module = stuff[0]
        assessment_1 = Assessment.objects.create(
            module=module,
            title="Assessment 1",
            value=50
        )
        assessment_2 = Assessment.objects.create(
            module=module,
            title="Assessment 2",
            value=50
        )
        student1 = stuff[1]
        student2 = stuff[2]
        student3 = stuff[3]
        performance1 = Performance.objects.get(module=module, student=student1)
        assessment_result1_1 = AssessmentResult.objects.create(
            assessment=assessment_1,
            mark=59
        )
        assessment_result1_2 = AssessmentResult.objects.create(
            assessment=assessment_2,
            mark=59
        )
        performance1.assessment_results.add(assessment_result1_1)
        performance1.assessment_results.add(assessment_result1_2)
        performance1.calculate_average()
        performance2 = Performance.objects.get(module=module, student=student2)
        assessment_result2_1 = AssessmentResult.objects.create(
            assessment=assessment_1,
            mark=54
        )
        assessment_result2_2 = AssessmentResult.objects.create(
            assessment=assessment_2,
            mark=54
        )
        performance2.assessment_results.add(assessment_result2_1)
        performance2.assessment_results.add(assessment_result2_2)
        performance2.calculate_average()
        performance3 = Performance.objects.get(module=module, student=student3)
        performance3.calculate_average()
        all_nines = module.get_all_performances_with_9()
        self.assertTrue(performance1 in all_nines)
        self.assertFalse(performance2 in all_nines)
        self.assertFalse(performance3 in all_nines)


class PerformanceTest(TeacherUnitTest):
    """Tests for the Performance class"""

    def test_enlisting_a_student_in_a_module_creates_performance_item(self):
        student = create_student()
        module = create_module()
        request = self.factory.post(
            '/add_students_to_module/%s/%s/' % (module.code, module.year),
            data={'student_ids': [student.student_id, ]}
        )
        request.user = self.user
        add_students_to_module(request, module.code, module.year)
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
            mark=20
        )
        performance1.assessment_results.add(result)
        assessment = Assessment.objects.create(
            title="Assessment 2",
            value=20
        )
        module.assessments.add(assessment)
        result = AssessmentResult.objects.create(
            assessment=assessment,
            mark=30
        )
        performance1.assessment_results.add(result)
        assessment = Assessment.objects.create(
            title="Assessment 3",
            value=20,
        )
        module.assessments.add(assessment)
        result = AssessmentResult.objects.create(
            assessment=assessment,
            mark=40
        )
        performance1.assessment_results.add(result)
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
            mark=50
        )
        performance2.assessment_results.add(result)
        assessment = Assessment.objects.create(
            title="And another assessment",
            value=10
        )
        module2.assessments.add(assessment)
        result = AssessmentResult.objects.create(
            assessment=assessment,
            mark=35,
            resit_mark=38,
            concessions='G',
            second_resit_mark=40
        )
        performance2.assessment_results.add(result)
        assessment = Assessment.objects.create(
            title="Middle Assessment",
            value=10
        )
        module2.assessments.add(assessment)
        expected_list_2 = [
            '35 (Submission: 38, Second Resubmission: 40)',
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

    def test_performance_returns_all_assessment_tpls(self):
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
            mark=20
        )
        performance1.assessment_results.add(result)
        assessment = Assessment.objects.create(
            title="Assessment 2",
            value=20
        )
        module.assessments.add(assessment)
        result = AssessmentResult.objects.create(
            assessment=assessment,
            mark=30
        )
        performance1.assessment_results.add(result)
        assessment = Assessment.objects.create(
            title="Assessment 3",
            value=20,
        )
        module.assessments.add(assessment)
        result = AssessmentResult.objects.create(
            assessment=assessment,
            mark=40
        )
        performance1.assessment_results.add(result)
        assessment = Assessment.objects.create(
            title="Exam",
            value=40
        )
        module.assessments.add(assessment)
        # No result for the exam - should return "None"
        expected_list_1 = [
            ('Assessment 1', '20'),
            ('Assessment 2', '30'),
            ('Assessment 3', '40'),
            ('Exam', None),
            ('<strong>Result</strong>', None)
        ]

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
            mark=50
        )
        performance2.assessment_results.add(result)
        assessment = Assessment.objects.create(
            title="A",
            value=10
        )
        module2.assessments.add(assessment)
        result = AssessmentResult.objects.create(
            assessment=assessment,
            mark=35,
            resit_mark=38,
            concessions='G',
            second_resit_mark=40
        )
        performance2.assessment_results.add(result)
        assessment = Assessment.objects.create(
            title="Middle Assessment",
            value=10
        )
        module2.assessments.add(assessment)
        expected_list_2 = [
            ('A', '35 (Submission: 38, Second Resubmission: 40)'),
            ('Middle Assessment', None),
            ('Zo far back in the alphabet', '50'),
            ('<strong>Result</strong>', None)
        ]
        self.assertEqual(
            performance1.all_assessment_results_as_tpls(),
            expected_list_1
        )
        self.assertEqual(
            performance2.all_assessment_results_as_tpls(),
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

    def test_marks_can_be_set_over_performance_functions(self):
        module = Module.objects.create(code="ML3", year=2014, title="ML")
        module.teachers.add(self.user.staff)
        assessment1 = Assessment.objects.create(
            module=module,
            title="Essay",
            value=30
        )
        assessment2 = Assessment.objects.create(
            module=module,
            title="Exam",
            value=70
        )
        student = Student.objects.create(
            first_name="Bugs",
            last_name="Bunny",
            student_id="bb23"
        )
        student.modules.add(module)
        performance = Performance.objects.create(
            module=module, student=student)
        performance.set_assessment_result('essay', 48)
        result = AssessmentResult.objects.first()
        self.assertEqual(result.mark, 48)
        performance.set_assessment_result('exam', 60)
        self.assertEqual(AssessmentResult.objects.count(), 2)
        second_result = AssessmentResult.objects.get(
            assessment=assessment2, part_of=performance)
        self.assertEqual(second_result.mark, 60)
        performance.set_assessment_result('essay', 50, 'resit')
        result = AssessmentResult.objects.get(
            assessment__slug='essay', part_of=performance)
        self.assertEqual(result.mark, 48)
        self.assertEqual(result.resit_mark, 50)
        self.assertEqual(result.result(), 50)

    def test_average_is_calculated_when_mark_is_set(self):
        module = Module.objects.create(code="ML3", year=2014, title="ML")
        module.teachers.add(self.user.staff)
        assessment1 = Assessment.objects.create(
            module=module,
            title="Essay",
            value=30
        )
        assessment2 = Assessment.objects.create(
            module=module,
            title="Exam",
            value=70
        )
        student = Student.objects.create(
            first_name="Bugs",
            last_name="Bunny",
            student_id="bb23"
        )
        student.modules.add(module)
        performance = Performance.objects.create(
            module=module, student=student)
        performance.set_assessment_result('essay', 48)
        self.assertEqual(performance.real_average, 14.4)
        self.assertEqual(performance.average, 14)

    def test_average_calculation_does_not_give_errors_when_mark_is_None(self):
        module = Module.objects.create(code="ML3", year=2014, title="ML")
        module.teachers.add(self.user.staff)
        assessment1 = Assessment.objects.create(
            module=module,
            title="Essay",
            value=30
        )
        assessment2 = Assessment.objects.create(
            module=module,
            title="Exam",
            value=70
        )
        student = Student.objects.create(
            first_name="Bugs",
            last_name="Bunny",
            student_id="bb23"
        )
        student.modules.add(module)
        performance = Performance.objects.create(
            module=module, student=student)
        performance.set_assessment_result('essay', None)
        self.assertEqual(performance.average, None)

    def test_set_and_get_marks_over_performance_functions(self):
        module = Module.objects.create(code="ML3", year=2014, title="ML")
        module.teachers.add(self.user.staff)
        assessment1 = Assessment.objects.create(
            module=module,
            title="Essay",
            value=30
        )
        assessment2 = Assessment.objects.create(
            module=module,
            title="Exam",
            value=70
        )
        student = Student.objects.create(
            first_name="Bugs",
            last_name="Bunny",
            student_id="bb23"
        )
        student.modules.add(module)
        performance = Performance.objects.create(
            module=module, student=student)
        performance.set_assessment_result('essay', 30)
        performance.set_assessment_result('exam', 60)
        self.assertEqual(performance.get_assessment_result('exam'), 60)
        self.assertEqual(performance.get_assessment_result('essay'), 30)
        performance.set_assessment_result('essay', 35, 'resit')
        performance.set_assessment_result('essay', 38, 'second_resit')
        result = performance.get_assessment_result('essay', 'string')
        self.assertEqual(
            result, '30 (Resubmission: 35, Second Resubmission: 38)')

    def test_all_results_with_feedback_function(self):
        module = Module.objects.create(code="ML3", year=2014, title="ML")
        module.teachers.add(self.user.staff)
        assessment_1 = Assessment.objects.create(
            module=module,
            title="Essay",
            value=20,
            marksheet_type='ESSAY',
            marksheet_type_resit='ESSAY'
        )
        assessment_2 = Assessment.objects.create(
            module=module,
            title="Presentation",
            value=30,
            marksheet_type='PRESENTATION',
            marksheet_type_resit='ESSAY'
        )
        assessment_3 = Assessment.objects.create(
            module=module,
            title="Exam",
            value=50,
        )
        student = Student.objects.create(
            first_name="Bugs",
            last_name="Bunny",
            student_id="bb23"
        )
        student.modules.add(module)
        performance = Performance.objects.create(
            module=module, student=student)
        assessment_result_1 = AssessmentResult.objects.create(
            assessment=assessment_1,
            mark=50,
        )
        performance.assessment_results.add(assessment_result_1)
        assessment_result_2 = AssessmentResult.objects.create(
            assessment=assessment_2,
            mark=38,
        )
        performance.assessment_results.add(assessment_result_2)
        assessment_result_3 = AssessmentResult.objects.create(
            assessment=assessment_3,
            mark=38,
            resit_mark=41
        )
        performance.assessment_results.add(assessment_result_3)
        all_results = performance.all_assessment_results_with_feedback()
        expected_1 = {
            'first': (
                50,
                '/individual_feedback/ML3/2014/essay/bb23/first/',
                None
            )
        }
        expected_2 = {
            'first': (
                38,
                '/individual_feedback/ML3/2014/presentation/bb23/first/',
                None
            ),
            'resit': (
                None,
                '/individual_feedback/ML3/2014/presentation/bb23/resit/',
                None
            )
        }
        expected_3 = {
            'first': (
                38,
                None,
                None
            ),
            'resit': (
                41,
                None,
                None
            )
        }
        self.assertEqual(
            performance.all_assessment_results_with_feedback(),
            [expected_1, expected_2, expected_3]
        )

    def test_resit_required_gets_shown(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student1 = stuff[1]
        student2 = stuff[2]
        performance1 = Performance.objects.get(
            module=module, student=student1
        )
        performance2 = Performance.objects.get(
            module=module, student=student2
        )
        assessment1 = Assessment.objects.create(
            module=module,
            title='Essay',
            value=20
        )
        assessment2 = Assessment.objects.create(
            module=module,
            title='Presentation',
            value=30
        )
        assessment3 = Assessment.objects.create(
            module=module,
            title='Exam',
            value=50
        )
        result1_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=42
        )
        result1_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=35
        )
        result1_3 = AssessmentResult.objects.create(
            assessment=assessment3,
            mark=42
        )
        performance1.assessment_results.add(result1_1)
        performance1.assessment_results.add(result1_2)
        performance1.assessment_results.add(result1_3)
        # Student 1 should pass!
        result2_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=35,
        )
        result2_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=42
        )
        result2_3 = AssessmentResult.objects.create(
            assessment=assessment3,
            mark=38,
            concessions='G'
        )
        performance2.assessment_results.add(result2_1)
        performance2.assessment_results.add(result2_2)
        performance2.assessment_results.add(result2_3)
        # Student 2 should fail
        self.assertFalse(performance1.resit_required())
        self.assertEqual(
            performance2.resit_required(),
            {assessment1: 'N', assessment3: 'G'}
        )

    def test_resit_required_gets_shown_for_concessions(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student1 = stuff[1]
        student2 = stuff[2]
        performance1 = Performance.objects.get(
            module=module, student=student1
        )
        performance2 = Performance.objects.get(
            module=module, student=student2
        )
        assessment1 = Assessment.objects.create(
            module=module,
            title='Essay',
            value=20
        )
        assessment2 = Assessment.objects.create(
            module=module,
            title='Presentation',
            value=30
        )
        assessment3 = Assessment.objects.create(
            module=module,
            title='Exam',
            value=50
        )
        result1_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=42
        )
        result1_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=44,
            concessions='G'
        )
        result1_3 = AssessmentResult.objects.create(
            assessment=assessment3,
            mark=42,
            concessions='P'
        )
        performance1.assessment_results.add(result1_1)
        performance1.assessment_results.add(result1_2)
        performance1.assessment_results.add(result1_3)
        self.assertEqual(
            performance1.resit_required(),
            {assessment2: 'G', assessment3: 'P'}
        )

    def test_qld_resit_required_shows_properly(self):
        stuff = set_up_stuff()
        module1 = stuff[0]
        student1 = stuff[1]
        student1.qld = True
        student1.save()
        student2 = stuff[2]
        student2.qld = False
        student2.save()
        # Test for foundational module
        module1.foundational = True
        module1.save()
        performance1 = Performance.objects.get(
            module=module1, student=student1
        )
        performance2 = Performance.objects.get(
            module=module1, student=student2
        )
        assessment1 = Assessment.objects.create(
            module=module1,
            title='Essay',
            value=20
        )
        assessment2 = Assessment.objects.create(
            module=module1,
            title='Presentation',
            value=30
        )
        assessment3 = Assessment.objects.create(
            module=module1,
            title='Exam',
            value=50
        )
        result1_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=70
        )
        result1_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=38
        )
        result1_3 = AssessmentResult.objects.create(
            assessment=assessment3,
            mark=70
        )
        performance1.assessment_results.add(result1_1)
        performance1.assessment_results.add(result1_2)
        performance1.assessment_results.add(result1_3)
        result2_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=70
        )
        result2_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=38
        )
        result2_3 = AssessmentResult.objects.create(
            assessment=assessment3,
            mark=70
        )
        performance2.assessment_results.add(result2_1)
        performance2.assessment_results.add(result2_2)
        performance2.assessment_results.add(result2_3)
        self.assertEqual(performance1.qld_resit_required(), [assessment2])
        self.assertEqual(performance2.qld_resit_required(), False)
        # Test for non-foundational module
        module1.foundational = False
        module1.save()
        performance1 = Performance.objects.get(
            module=module1, student=student1
        )
        performance2 = Performance.objects.get(
            module=module1, student=student2
        )
        self.assertEqual(performance1.qld_resit_required(), False)
        self.assertEqual(performance2.qld_resit_required(), False)

#    def test_second_resit_required_gets_shown(self):
#        stuff = set_up_stuff()
#        module = stuff[0]
#        student1 = stuff[1]
#        student2 = stuff[2]
#        performance1 = Performance.objects.get(
#            module=module, student=student1
#        )
#        performance2 = Performance.objects.get(
#            module=module, student=student2
#        )
#        assessment1 = Assessment.objects.create(
#            module=module,
#            title='Essay',
#            value=20
#        )
#        assessment2 = Assessment.objects.create(
#            module=module,
#            title='Presentation',
#            value=30
#        )
#        assessment3 = Assessment.objects.create(
#            module=module,
#            title='Exam',
#            value=50
#        )
#        result1_1 = AssessmentResult.objects.create(
#            assessment=assessment1,
#            mark=38,
#            resit_mark=40
#        )
#        result1_2 = AssessmentResult.objects.create(
#            assessment=assessment2,
#            mark=42
#        )
#        result1_3 = AssessmentResult.objects.create(
#            assessment=assessment3,
#            mark=36,
#            resit_mark=36
#        )
#        performance1.assessment_results.add(result1_1)
#        performance1.assessment_results.add(result1_2)
#        performance1.assessment_results.add(result1_3)
#        self.assertEqual(
#            performance1.second_resit_required(),
#            [assessment3]
#        )


class AssessmentResultTest(TeacherUnitTest):
    """Testing the Assessment Result class"""

    def test_result_returns_highest_mark(self):
        module = Module.objects.create(code="ML3", year=2014, title="ML")
        module.teachers.add(self.user.staff)
        assessment = Assessment.objects.create(
            module=module,
            title="Dissertation",
            value=100
        )
        student = Student.objects.create(
            first_name="Bugs",
            last_name="Bunny",
            student_id="bb23"
        )
        student.modules.add(module)
        performance = Performance.objects.create(
            module=module, student=student)
        assessment_result_1 = AssessmentResult.objects.create(
            assessment=assessment,
            mark=38,
            resit_mark=42
        )
        performance.assessment_results.add(assessment_result_1)
        self.assertEqual(assessment_result_1.result(), 42)
        assessment_result_2 = AssessmentResult.objects.create(
            assessment=assessment,
            mark=38,
            resit_mark=36
        )
        performance.assessment_results.add(assessment_result_2)
        self.assertEqual(assessment_result_2.result(), 38)

    def test_qld_status_is_returned_correctly(self):
        module = Module.objects.create(code="ML3", year=2014, title="ML")
        module.teachers.add(self.user.staff)
        assessment = Assessment.objects.create(
            module=module,
            title="Dissertation",
            value=100
        )
        student = Student.objects.create(
            first_name="Bugs",
            last_name="Bunny",
            student_id="bb23"
        )
        student.modules.add(module)
        performance = Performance.objects.create(
            module=module, student=student)
        assessment_result_1 = AssessmentResult.objects.create(
            assessment=assessment,
            mark=38,
            resit_mark=42
        )
        performance.assessment_results.add(assessment_result_1)
        assessment_result_2 = AssessmentResult.objects.create(
            assessment=assessment,
            mark=38,
            resit_mark=36
        )
        performance.assessment_results.add(assessment_result_2)
        assessment_result_3 = AssessmentResult.objects.create(
            assessment=assessment,
            mark=38,
            resit_mark=35,
            second_resit_mark=33,
            qld_resit=45
        )  # Only 3 attempts should be counted
        performance.assessment_results.add(assessment_result_3)
        assessment_result_4 = AssessmentResult.objects.create(
            assessment=assessment,
            mark=38,
            resit_mark=35,
            qld_resit=45
        )
        performance.assessment_results.add(assessment_result_4)
        self.assertEqual(assessment_result_1.no_qld_problems(), True)
        self.assertEqual(assessment_result_2.no_qld_problems(), False)
        self.assertEqual(assessment_result_3.no_qld_problems(), False)
        self.assertEqual(assessment_result_4.no_qld_problems(), True)

    def test_result_with_feedback_function(self):
        module = Module.objects.create(code="ML3", year=2014, title="ML")
        module.teachers.add(self.user.staff)
        assessment = Assessment.objects.create(
            module=module,
            title="Essay",
            value=100,
            marksheet_type='ESSAY',
            marksheet_type_resit='ESSAY'
        )
        student = Student.objects.create(
            first_name="Bugs",
            last_name="Bunny",
            student_id="bb23"
        )
        student.modules.add(module)
        performance = Performance.objects.create(
            module=module, student=student)
        assessment_result_1 = AssessmentResult.objects.create(
            assessment=assessment,
            mark=50,
        )
        performance.assessment_results.add(assessment_result_1)
        assessment_result_2 = AssessmentResult.objects.create(
            assessment=assessment,
            mark=38,
        )
        performance.assessment_results.add(assessment_result_2)
        assessment_result_3 = AssessmentResult.objects.create(
            assessment=assessment,
            mark=38,
            resit_mark=41
        )
        performance.assessment_results.add(assessment_result_3)
        result_1 = assessment_result_1.result_with_feedback()
        expected_1 = {
            'first': (
                50,
                '/individual_feedback/ML3/2014/essay/bb23/first/',
                None
            )
        }
        self.assertEqual(result_1, expected_1)
        self.assertFalse(assessment_result_1.eligible_for_resit())
        result_2 = assessment_result_2.result_with_feedback()
        self.assertTrue(assessment_result_2.eligible_for_resit())
        expected_2 = {
            'first': (
                38,
                '/individual_feedback/ML3/2014/essay/bb23/first/',
                None
            ),
            'resit': (
                None,
                '/individual_feedback/ML3/2014/essay/bb23/resit/',
                None
            )
        }
        self.assertEqual(result_2, expected_2)
        result_3 = assessment_result_3.result_with_feedback()
        expected_3 = {
            'first': (
                38,
                '/individual_feedback/ML3/2014/essay/bb23/first/',
                None
            ),
            'resit': (
                41,
                '/individual_feedback/ML3/2014/essay/bb23/resit/',
                None
            )
        }
        self.assertEqual(result_3, expected_3)

    def test_get_marksheet_urls_returns_right_urls(self):
        module1 = create_module()
        student = create_student()
        performance1 = Performance.objects.create(
            student=student, module=module1)
        assessment1 = Assessment.objects.create(
            module=module1,
            value=50,
            title='Essay'
        )
        assessment_result_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=30,
            resit_mark=40,
        )
        performance1.assessment_results.add(assessment_result_1)
        feedback_1_1 = IndividualFeedback.objects.create(
            assessment_result=assessment_result_1,
            attempt='first',
            completed=True
        )
        feedback_1_2 = IndividualFeedback.objects.create(
            assessment_result=assessment_result_1,
            attempt='resit',
            completed=True
        )
        link1 = (
            '/export_feedback/' +
            module1.code +
            '/' +
            str(module1.year) +
            '/' +
            assessment1.slug +
            '/' +
            student.student_id +
            '/first/'
        )
        link2 = (
            '/export_feedback/' +
            module1.code +
            '/' +
            str(module1.year) +
            '/' +
            assessment1.slug +
            '/' +
            student.student_id +
            '/resit/'
        )
        self.assertEqual(
            assessment_result_1.get_marksheet_urls(),
            {'first': link1, 'resit': link2}
        )

    def test_set_one_mark_sets_mark_and_timestamp(self):
        module = create_module()
        student = create_student()
        performance = Performance.objects.create(
            student=student, module=module)
        assessment = Assessment.objects.create(
            module=module,
            value=50,
            title='Essay'
        )
        assessment_result = AssessmentResult.objects.create(
            assessment=assessment,
            mark=30,
            resit_mark=40,
        )
        time_of_saving = timezone.now()
        assessment_result.set_one_mark('first', 35)
        result_out = AssessmentResult.objects.first()
        self.assertEqual(result_out.mark, 35)
        saved_time = result_out.last_modified
        difference = saved_time - time_of_saving
        self.assertTrue(difference.seconds<1)


class ConsistencyTest(TeacherUnitTest):
    """Tests to ensure that different model parts work together"""

    def test_model_and_performance_as_tpls_are_the_same(self):
        module = create_module()
        student = create_student()
        performance = Performance.objects.create(
            module=module, student=student)
        assessment1 = Assessment.objects.create(
            module=module,
            title="Assessment 1",
            value=20
        )
        assessment2 = Assessment.objects.create(
            module=module,
            title="Exam",
            value=20
        )
        assessment3 = Assessment.objects.create(
            module=module,
            title="Assessment 2",
            value=20
        )
        assessment4 = Assessment.objects.create(
            module=module,
            title="Assessment 3",
            value=20
        )
        assessment5 = Assessment.objects.create(
            module=module,
            title="Assessment 4",
            value=20
        )
        result1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=10
        )
        performance.assessment_results.add(result1)
        result2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=20
        )
        performance.assessment_results.add(result2)
        result3 = AssessmentResult.objects.create(
            assessment=assessment3,
            mark=30
        )
        performance.assessment_results.add(result3)
        result4 = AssessmentResult.objects.create(
            assessment=assessment4,
            mark=40
        )
        performance.assessment_results.add(result4)
        result5 = AssessmentResult.objects.create(
            assessment=assessment5,
            mark=50
        )
        performance.assessment_results.add(result5)
        all_assessments = module.all_assessment_titles()
        all_results = performance.all_assessment_results_as_tpls()
        counter = 0
        for assessment in all_assessments:
            self.assertEqual(assessment[0], all_results[counter][0])
            counter += 1
