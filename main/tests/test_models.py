from main.models import *
from main.views import *
from django.core.exceptions import ValidationError
from django.test import TestCase
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
                False
            )
        }
        expected_2 = {
            'first': (
                38,
                '/individual_feedback/ML3/2014/presentation/bb23/first/',
                False
            ),
            'resit': (
                None,
                '/individual_feedback/ML3/2014/presentation/bb23/resit/',
                False
            )
        }
        expected_3 = {
            'first': (
                38,
                False,
                False
            ),
            'resit': (
                41,
                False,
                False
            )
        }
        self.assertEqual(
            performance.all_assessment_results_with_feedback(),
            [expected_1, expected_2, expected_3]
        )



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
                False
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
                False
            ),
            'resit': (
                None,
                '/individual_feedback/ML3/2014/essay/bb23/resit/',
                False
            )
        }
        self.assertEqual(result_2, expected_2)
        result_3 = assessment_result_3.result_with_feedback()
        expected_3 = {
            'first': (
                38,
                '/individual_feedback/ML3/2014/essay/bb23/first/',
                False
            ),
            'resit': (
                41,
                '/individual_feedback/ML3/2014/essay/bb23/resit/',
                False
            )
        }
        self.assertEqual(result_3, expected_3)
