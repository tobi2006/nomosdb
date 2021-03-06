from django.test import TestCase, RequestFactory
from main.models import *
from main.views import *
from bs4 import BeautifulSoup
from .base import *
import datetime
from feedback.models import IndividualFeedback


class StatusCheckTest(TestCase):
    """Testing the decorator test functions"""

    def test_user_teacher_test_works(self):
        elmar = create_teacher()
        self.assertTrue(is_staff(elmar.user))
        self.assertTrue(is_teacher(elmar.user))
        self.assertFalse(is_admin(elmar.user))
        self.assertFalse(is_student(elmar.user))

    def test_staff_admin_status_is_properly_undertood_at_login(self):
        admin = create_admin()
        self.assertTrue(is_staff(admin.user))
        self.assertFalse(is_teacher(admin.user))
        self.assertTrue(is_admin(admin.user))
        self.assertFalse(is_student(admin.user))

    def test_student_is_student_and_neither_admin_nor_teacher(self):
        bugs_user = User.objects.create_user(
            username='bb42', password='ilovecarrots')
        bugs = Student.objects.create(
            student_id='bb42',
            last_name='Bunny',
            first_name='Bugs',
            user=bugs_user
        )
        self.assertTrue(is_student(bugs_user))
        self.assertFalse(is_staff(bugs_user))
        self.assertFalse(is_admin(bugs_user))
        self.assertFalse(is_teacher(bugs_user))


class HomePageTest(TeacherUnitTest):
    """Simple tests for the home page"""

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_title_contains_uni_name(self):
        response = self.client.get('/')
        self.assertContains(response, 'Acme University')


class HomePageForStudentTest(StudentUnitTest):
    """Student homepage is shown"""

    def test_student_home_shows_student_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'student_home.html')

    def test_student_sees_links_to_all_marksheets(self):
        student = self.user.student
        module1 = create_module()
        performance1 = Performance.objects.create(
            student=student, module=module1)
        assessment1 = Assessment.objects.create(
            module=module1,
            value=50,
            title='Essay',
            available=True,
            resit_available=True
        )
        assessment2 = Assessment.objects.create(
            module=module1,
            value=50,
            title='Exam',
            available=True
        )
        assessment_result_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=30,
            resit_mark=40,
        )
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
        performance1.assessment_results.add(assessment_result_1)
        link1 = (
            '<a href="/export_feedback/' +
            module1.code +
            '/' +
            str(module1.year) +
            '/' +
            assessment1.slug +
            '/' +
            student.student_id +
            '/'
        )
        link1_1 = link1 + 'first/'
        link1_2 = link1 + 'resit/'
        assessment_result_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=30,
            resit_mark=40,
        )
        feedback_2_1 = IndividualFeedback.objects.create(
            assessment_result=assessment_result_2,
            attempt='first',
            completed=True
        )
        performance1.assessment_results.add(assessment_result_2)
        link2_1 = (
            '<a href="/export_feedback/' +
            module1.code +
            '/' +
            str(module1.year) +
            '/' +
            assessment2.slug +
            '/' +
            student.student_id +
            '/first/'
        )
        module2 = Module.objects.create(
            title="Introduction to Squaredance",
            year=1901,
            code='i2sq42'
        )
        student.modules.add(module2)
        performance2 = Performance.objects.create(
            student=student, module=module2)
        assessment3 = Assessment.objects.create(
            module=module2,
            value=50,
            title='Essay',
            available=False,
            resit_available=False
        )
        assessment_result_3 = AssessmentResult.objects.create(
            assessment=assessment3,
            mark=30,
            resit_mark=40,
        )
        feedback_3_1 = IndividualFeedback.objects.create(
            assessment_result=assessment_result_3,
            attempt='first',
            completed=True
        )
        feedback_3_2 = IndividualFeedback.objects.create(
            assessment_result=assessment_result_3,
            attempt='resit',
            completed=True
        )
        performance2.assessment_results.add(assessment_result_3)
        link3 = (
            '<a href="/export_feedback/' +
            module2.code +
            '/' +
            str(module2.year) +
            '/' +
            assessment3.slug +
            '/' +
            student.student_id
        )
        link3_1 = link3 + '/first/'
        link3_2 = link3 + '/resit/'
        assessment4 = Assessment.objects.create(
            module=module2,
            value=50,
            title='Exam',
            available=False
        )
        assessment_result_4 = AssessmentResult.objects.create(
            assessment=assessment4,
            mark=30,
            resit_mark=40,
        )
        feedback_4_1 = IndividualFeedback.objects.create(
            assessment_result=assessment_result_4,
            attempt='first',
            completed=True
        )
        performance2.assessment_results.add(assessment_result_4)
        link4_1 = (
            '<a href="/export_feedback/' +
            module2.code +
            '/' +
            str(module2.year) +
            '/' +
            assessment2.slug +
            '/' +
            student.student_id +
            '/first/'
        )
        response = self.client.get('/')
        self.assertContains(response, link1_1)
        self.assertContains(response, link1_2)
        self.assertContains(response, link2_1)
        self.assertNotContains(response, link3_1)
        self.assertNotContains(response, link3_2)
        self.assertNotContains(response, link4_1)


class AdminDashboardTest(AdminUnitTest):
    """Checks the Admin Dashboard"""

    def test_admin_page_uses_right_template(self):
        response = self.client.get('/admin_dashboard/')
        self.assertNotContains(response, 'Main Settings')
        self.user.staff.main_admin = True
        self.user.staff.save()
        response = self.client.get('/admin_dashboard/')
        self.assertContains(response, 'Main Settings')

    def test_admin_page_shows_all_subjects_and_years_for_main_admin(self):
        self.user.staff.main_admin = True
        self.user.staff.save()
        subject_area_1 = SubjectArea.objects.create(name='Cartoon Studies')
        subject_area_2 = SubjectArea.objects.create(name='Evil Plotting')
        course_1 = Course.objects.create(
            title='BA in Cartoon Studies',
            short_title='Cartoon Studies',
        )
        course_1.subject_areas.add(subject_area_1)
        course_2 = Course.objects.create(
            title='BA in Evil Plotting',
            short_title='Evil Plotting',
        )
        course_2.subject_areas.add(subject_area_2)
        course_3 = Course.objects.create(
            title='BA in Cartoon Studies with Evil Plotting',
            short_title='Cartoon Studies / Evil Plotting',
        )
        course_3.subject_areas.add(subject_area_1)
        course_3.subject_areas.add(subject_area_2)
        stuff = set_up_stuff()
        student_1 = stuff[1]
        student_1.course = course_1
        student_1.year = 1
        student_1.save()
        student_2 = stuff[2]
        student_2.course = course_2
        student_2.year = 2
        student_2.save()
        student_3 = stuff[3]
        student_3.course = course_3
        student_3.year = 3
        student_3.save()
        response = self.client.get('/admin_dashboard/')
        url = (
            '<a href="/assign_tutors/' +
            subject_area_1.slug +
            '/1/">'
        )
        self.assertContains(response, url)
        url = (
            '<a href="/assign_tutors/' +
            subject_area_1.slug +
            '/2/">'
        )
        self.assertNotContains(response, url)
        url = (
            '<a href="/assign_tutors/' +
            subject_area_1.slug +
            '/3/">'
        )
        self.assertContains(response, url)
        url = (
            '<a href="/assign_tutors/' +
            subject_area_2.slug +
            '/1/">'
        )
        self.assertNotContains(response, url)
        url = (
            '<a href="/assign_tutors/' +
            subject_area_2.slug +
            '/2/">'
        )
        self.assertContains(response, url)
        url = (
            '<a href="/assign_tutors/' +
            subject_area_2.slug +
            '/3/">'
        )
        self.assertContains(response, url)

    def test_admin_page_shows_own_subjects_and_years_for_normal_admin(self):
        subject_area_1 = SubjectArea.objects.create(name='Cartoon Studies')
        self.user.staff.subject_areas.add(subject_area_1)
        subject_area_2 = SubjectArea.objects.create(name='Evil Plotting')
        course_1 = Course.objects.create(
            title='BA in Cartoon Studies',
            short_title='Cartoon Studies',
        )
        course_1.subject_areas.add(subject_area_1)
        course_2 = Course.objects.create(
            title='BA in Evil Plotting',
            short_title='Evil Plotting',
        )
        course_2.subject_areas.add(subject_area_2)
        course_3 = Course.objects.create(
            title='BA in Cartoon Studies with Evil Plotting',
            short_title='Cartoon Studies / Evil Plotting',
        )
        course_3.subject_areas.add(subject_area_1)
        course_3.subject_areas.add(subject_area_2)
        stuff = set_up_stuff()
        student_1 = stuff[1]
        student_1.course = course_1
        student_1.year = 1
        student_1.save()
        student_2 = stuff[2]
        student_2.course = course_2
        student_2.year = 2
        student_2.save()
        student_3 = stuff[3]
        student_3.course = course_3
        student_3.year = 3
        student_3.save()
        response = self.client.get('/admin_dashboard/')
        url = (
            '<a href="/assign_tutors/' +
            subject_area_1.slug +
            '/1/">'
        )
        self.assertContains(response, url)
        url = (
            '<a href="/assign_tutors/' +
            subject_area_1.slug +
            '/2/">'
        )
        self.assertNotContains(response, url)
        url = (
            '<a href="/assign_tutors/' +
            subject_area_1.slug +
            '/3/">'
        )
        self.assertContains(response, url)
        url = (
            '<a href="/assign_tutors/' +
            subject_area_2.slug +
            '/1/">'
        )
        self.assertNotContains(response, url)
        url = (
            '<a href="/assign_tutors/' +
            subject_area_2.slug +
            '/2/">'
        )
        self.assertNotContains(response, url)
        url = (
            '<a href="/assign_tutors/' +
            subject_area_2.slug +
            '/3/">'
        )
        self.assertNotContains(response, url)


class StudentViewTest(TeacherUnitTest):
    """Tests for the student view function"""

    def test_student_view_renders_student_view_template(self):
        student = create_student()
        response = self.client.get(student.get_absolute_url())
        self.assertTemplateUsed(response, 'student_view.html')
        self.assertContains(response, "bb23")
        self.assertContains(response, "Bunny")
        self.assertContains(response, "Bugs")


class AddEditStudentTest(TeacherUnitTest):
    """Tests for the student form function"""

    def send_form(self):
        response = self.client.post(
            '/add_student/',
            data={
                'student_id': 'bb23',
                'last_name': 'Bünny',
                'first_name': 'Bugs Middle Names'
            }
        )
        return response

    def test_add_edit_student_renders_right_template(self):
        response = self.client.get('/add_student/')
        self.assertTemplateUsed(response, 'student_form.html')

    def test_add_student_adds_student_to_database(self):
        self.send_form()
        student = Student.objects.first()
        self.assertEqual(student.student_id, 'bb23')
        self.assertEqual(student.last_name, 'Bünny')
        self.assertEqual(student.first_name, 'Bugs Middle Names')

    def test_edit_student_shows_correct_data(self):
        student = create_student()
        response = self.client.get(student.get_edit_url())
        self.assertTemplateUsed(response, 'student_form.html')
        self.assertContains(response, 'Bunny')
        self.assertContains(response, 'Bugs')
        self.assertContains(response, 'bb23')


class InviteStudentTest(AdminUnitTest):
    """Already added students can be invited"""

    def test_students_can_be_invited_users_get_created(self):
        subject_area = create_subject_area()
        course = Course.objects.create(
            title='BA in Cartoon Studies',
            short_title='BA CS',
        )
        course.subject_areas.add(subject_area)
        course.save()
        student1 = create_student()
        student1.email = 'bb23@acme.edu'
        student1.save()
        student2 = Student.objects.create(
            student_id='bb4223',
            first_name='Buster Middle Names',
            last_name='Bunny',
            email='bb4223@acme.edu',
            year=2,
            course=course
        )
        url = '/invite_students/' + subject_area.slug + '/'
        request = self.factory.post(
            url,
            data={
                'selected_student_id': [
                    student1.student_id,
                    student2.student_id
                ]
            }
        )
        request.user = self.user
        invite_students(request, subject_area.slug, testing=True)
        user1 = User.objects.get(username='bmnb1')
        user2 = User.objects.get(username='bmnb2')
        student1_out = Student.objects.get(student_id='bb23')
        student2_out = Student.objects.get(first_name='Buster Middle Names')
        self.assertEqual(student1_out.user, user1)
        self.assertEqual(student2_out.user, user2)

    def test_invitation_status_is_displayed_correctly(self):
        subject_area = create_subject_area()
        course = Course.objects.create(
            title='BA in Cartoon Studies',
            short_title='BA CS',
        )
        course.subject_areas.add(subject_area)
        course.save()
        student1 = create_student()  # No email address
        student2 = Student.objects.create(
            student_id='bb4223',
            first_name='Buster',
            last_name='Bunny',
            year=2,
            email='bb4423@acme.edu',
            course=course
        )
        url = '/invite_students/' + subject_area.slug + '/'
        request = self.factory.post(
            url,
            data={'selected_student_id': [
                student1.student_id, student2.student_id
                ]
            }
        )
        request.user = self.user
        response = invite_students(request, subject_area.slug, testing=True)
        soup = BeautifulSoup(response.content)
        added = str(soup.select('#students_added')[0])
        not_added = str(soup.select('#students_without_email')[0])
        self.assertIn(student1.name(), not_added)
        self.assertIn(student2.name(), added)


class StaffResetPasswordTest(AdminUnitTest):
    """Password can be reset by staff"""

    def test_staff_can_reset_password(self):
        request = self.factory.get(
            '/reset_password/',
            data={'email': self.user.email}
        )
        request.user = self.user
        response = reset_password(request, testing=True)
        self.assertContains(response, self.user.first_name)


class StudentResetPasswordTest(NotYetLoggedInUnitTest):

    def test_student_can_reset_password(self):
        user = User.objects.create_user(
            username='bb42', password='ilovecarrots')
        student = Student.objects.create(
            student_id='bb42',
            last_name='Bunny',
            first_name='Bugs',
            user=user,
            email='bb23@acme.edu'
        )
        request = self.factory.get(
            '/reset_password/',
            data={'email': student.email}
        )
        request.user = self.user
        response = reset_password(request, testing=True)
        self.assertContains(response, student.short_first_name())


class ModuleViewTest(TeacherUnitTest):
    """Tests for the module view"""

    def test_module_view_renders_module_view_template(self):
        module = Module.objects.create(
            title="Hunting Practice",
            code="hp23",
            year=1900
        )
        response = self.client.get(module.get_absolute_url())
        self.assertTemplateUsed(response, 'module_view.html')

    def test_performances_in_a_module_are_shown(self):
        module = Module.objects.create(
            title="Hunting Practice",
            code="hp23",
            year=1900,
            eligible="1"
        )
        student = Student.objects.create(
            last_name="Pig",
            first_name="Porky",
            student_id="pp2323",
            year=2
        )
        response = self.client.post(
            module.get_add_students_url(),
            data={'student_ids': [student.student_id]}
        )
        out_response = self.client.get(module.get_absolute_url())
        self.assertContains(out_response, "Pig, Porky")

    def test_only_active_students_appear_in_module_view(self):
        module = create_module()
        student1 = create_student()
        student2 = Student.objects.create(
            last_name="Pig",
            first_name="Porky",
            student_id="pp2323",
            active=False
        )
        student1.modules.add(module)
        performance1 = Performance.objects.create(
            student=student1, module=module)
        performance2 = Performance.objects.create(
            student=student2, module=module)
        student2.modules.add(module)
        response = self.client.get(module.get_absolute_url())
        self.assertContains(response, 'Bunny, Bugs')
        self.assertNotContains(response, 'Pig, Porky')

    def test_assessment_availability_is_shown_correctly(self):
        module = create_module()
        student = create_student()
        student.modules.add(module)
        performance = Performance.objects.create(
            student=student, module=module)
        assessment = Assessment.objects.create(
            title="Essay",
            value=100,
            available=False,
            marksheet_type="Something"
        )
        module.assessments.add(assessment)
        response = self.client.get(module.get_absolute_url())
        self.assertContains(
            response,
            '<span class="glyphicon glyphicon-eye-close">'
        )
        self.assertContains(
            response,
            'Show Essay to students'
        )
        assessment.available = True
        assessment.save()
        response = self.client.get(module.get_absolute_url())
        self.assertContains(
            response,
            '<span class="glyphicon glyphicon-eye-open">'
        )
        self.assertContains(
            response,
            'Hide Essay from students'
        )

    def test_only_assessments_with_marksheet_show_availability(self):
        module = create_module()
        student = create_student()
        student.modules.add(module)
        performance = Performance.objects.create(
            student=student, module=module)
        assessment1 = Assessment.objects.create(
            title="Essay",
            value=50,
            available=False,
            marksheet_type="Something"
        )
        assessment2 = Assessment.objects.create(
            title="Exam",
            value=50,
            available=False,
        )
        module.assessments.add(assessment1)
        module.assessments.add(assessment2)
        response = self.client.get(module.get_absolute_url())
        self.assertContains(
            response,
            'Show Essay to students'
        )
        self.assertNotContains(
            response,
            'Show Exam to students'
        )

    def test_resit_menu_shows_when_required(self):
        stuff = set_up_stuff()
        module = stuff[0]
        module.foundational = True
        module.save()
        student1 = stuff[1]
        student1.qld = True
        student1.save()
        student2 = stuff[2]
        student2.qld = True
        student2.save()
        performance1 = Performance.objects.get(
            module=module, student=student1
        )
        performance2 = Performance.objects.get(
            module=module, student=student2
        )
        assessment1 = Assessment.objects.create(
            module=module,
            title='Essay',
            value=50
        )
        assessment2 = Assessment.objects.create(
            module=module,
            title='Presentation',
            value=50
        )
        result1_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=42
        )
        result1_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=40
        )
        performance1.assessment_results.add(result1_1)
        performance1.assessment_results.add(result1_2)
        result2_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=60,
        )
        result2_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=80
        )
        performance2.assessment_results.add(result2_1)
        performance2.assessment_results.add(result2_2)
        response = self.client.get(module.get_absolute_url())
        resit_string = (
            '<a class = "btn btn-default dropdown-toggle" data-toggle' +
            '="dropdown">Resits <span class="caret"></span></a>'
        )
        self.assertNotContains(
            response,
            resit_string
        )
        result1_1.mark = 0
        result1_1.save()
        response = self.client.get(module.get_absolute_url())
        self.assertContains(
            response,
            resit_string
        )
        result1_1.mark = 50
        result1_1.save()
        result2_1.mark = 39
        result2_1.save()
        response = self.client.get(module.get_absolute_url())
        self.assertContains(
            response,
            resit_string
        )

    def test_two_resit_with_feedback_symbols_show(self):
        stuff = set_up_stuff()
        module = stuff[0]
        module.foundational = True
        module.save()
        student1 = stuff[1]
        student1.qld = True
        student1.save()
        performance1 = Performance.objects.get(
            module=module, student=student1
        )
        assessment1 = Assessment.objects.create(
            module=module,
            title='Essay',
            value=50,
            marksheet_type='ESSAY',
            resit_marksheet_type='ESSAY',
        )
        assessment2 = Assessment.objects.create(
            module=module,
            title='Presentation',
            value=50,
            marksheet_type='PRESENTATION',
            resit_marksheet_type='PRESENTATION',
        )
        result1_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=38,
            resit_mark=80
        )
        result1_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=36,
            resit_mark=80
        )
        performance1.assessment_results.add(result1_1)
        performance1.assessment_results.add(result1_2)

        resit_string_essay = (
            '<a href="/individual_feedback/' +
            stuff[0].code +
            '/' +
            str(stuff[0].year) +
            '/' +
            assessment1.slug +
            '/' +
            stuff[1].student_id +
            '/resit/">'
        )
        resit_string_presentation = (
            '<a href="/individual_feedback/' +
            stuff[0].code +
            '/' +
            str(stuff[0].year) +
            '/' +
            assessment2.slug +
            '/' +
            stuff[1].student_id +
            '/resit/">'
        )

        response = self.client.get(module.get_absolute_url())
        self.assertContains(
            response,
            resit_string_essay
        )
        self.assertContains(
            response,
            resit_string_presentation
        )

    def test_two_resit_with_feedback_symbols_show_with_3_assessments(self):
        stuff = set_up_stuff()
        module = stuff[0]
        module.save()
        student1 = stuff[1]
        student1.save()
        performance1 = Performance.objects.get(
            module=module, student=student1
        )
        assessment1 = Assessment.objects.create(
            module=module,
            title='Essay',
            value=25,
            marksheet_type='ESSAY',
            resit_marksheet_type='ESSAY',
        )
        assessment2 = Assessment.objects.create(
            module=module,
            title='Presentation',
            value=25,
            marksheet_type='PRESENTATION',
            resit_marksheet_type='PRESENTATION',
        )
        assessment3 = Assessment.objects.create(
            module=module,
            title='Second Essay',
            value=50,
            marksheet_type='ESSAY',
            resit_marksheet_type='ESSAY',
        )
        result1_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=30,
            resit_mark=80
        )
        result1_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=28,
            resit_mark=80
        )
        result1_3 = AssessmentResult.objects.create(
            assessment=assessment3,
            mark=40,
        )
        performance1.assessment_results.add(result1_1)
        performance1.assessment_results.add(result1_2)
        performance1.assessment_results.add(result1_3)

        resit_string_essay = (
            '<a href="/individual_feedback/' +
            stuff[0].code +
            '/' +
            str(stuff[0].year) +
            '/' +
            assessment1.slug +
            '/' +
            stuff[1].student_id +
            '/resit/">'
        )
        resit_string_presentation = (
            '<a href="/individual_feedback/' +
            stuff[0].code +
            '/' +
            str(stuff[0].year) +
            '/' +
            assessment2.slug +
            '/' +
            stuff[1].student_id +
            '/resit/">'
        )
        resit_string_second_essay = (
            '<a href="/individual_feedback/' +
            stuff[0].code +
            '/' +
            str(stuff[0].year) +
            '/' +
            assessment3.slug +
            '/' +
            stuff[1].student_id +
            '/resit/">'
        )

        response = self.client.get(module.get_absolute_url())
        self.assertContains(
            response,
            resit_string_essay
        )
        self.assertContains(
            response,
            resit_string_presentation
        )
        self.assertNotContains(
            response,
            resit_string_second_essay
        )

class AddStudentsToModuleTest(TeacherUnitTest):
    """Tests for the function to add students to a module"""

    def test_add_students_to_module_uses_right_template(self):
        module = create_module()
        response = self.client.get(module.get_add_students_url())
        self.assertTemplateUsed(response, 'add_students_to_module.html')

    def test_only_students_from_same_subject_areas_and_year_are_shown(self):
        subject_area1 = create_subject_area()
        subject_area2 = SubjectArea.objects.create(name="Evil Plotting")
        course = Course.objects.create(title="BA in Cartoon Studies")
        course.subject_areas.add(subject_area1)
        course.save()
        course2 = Course.objects.create(
            title="BA in Evil Plotting")
        course2.subject_areas.add(subject_area2)
        course2.save()
        module = create_module()
        module.subject_areas.add(subject_area1)
        module.save()
        student1 = create_student()
        student1.course = course
        student1.year = 1
        student1.save()
        student2 = Student.objects.create(
            last_name="Duck",
            first_name="Daffy",
            student_id="dd42",
            course=course2,
            year=1
        )
        student3 = Student.objects.create(
            last_name="Pig",
            first_name="Porky",
            student_id="pp2323",
            course=course,
            year=2
        )
        student4 = Student.objects.create(
            last_name="Runner",
            first_name="Road",
            student_id="rr42",
            course=course,
            year=1,
            active=False
        )
        response = self.client.get(module.get_add_students_url())
        self.assertContains(response, 'Bunny')
        self.assertNotContains(response, 'Duck')
        self.assertNotContains(response, 'Pig')
        self.assertNotContains(response, 'Runner')

    def test_submitting_an_empty_form_does_not_break_it(self):
        module = create_module()
        response = self.client.post(
            '/add_students_to_module/%s/%s' % (module.code, module.year),
            data={}
        )
        self.assertTrue(response.status_code in [301, 302])


class RemoveStudentFromModuleTest(TeacherUnitTest):
    """Tests for the function to remove a student from a module"""

    def test_student_removed_from_module_is_not_in_module_anymore(self):
        module = create_module()
        student = create_student()
        student.modules.add(module)
        Performance.objects.create(module=module, student=student)
        url = (
            '/remove_student_from_module/' +
            module.code +
            '/' +
            str(module.year) +
            '/' +
            student.student_id +
            '/'
        )
        request = self.factory.get(url)
        request.user = self.user
        response = remove_student_from_module(
            request, module.code, module.year, student.student_id)
        self.assertEqual(Performance.objects.count(), 0)
        self.assertEqual(student.modules.count(), 0)

    def test_assessment_results_are_deleted(self):
        module = create_module()
        student = create_student()
        student.modules.add(module)
        performance = Performance.objects.create(
            module=module, student=student)
        assessment = Assessment.objects.create(
            module=module,
            title='Essay'
        )
        result = AssessmentResult.objects.create(assessment=assessment)
        self.assertEqual(AssessmentResult.objects.count(), 1)
        performance.assessment_results.add(result)
        url = (
            '/remove_student_from_module/' +
            module.code +
            '/' +
            str(module.year) +
            '/' +
            student.student_id +
            '/'
        )
        response = self.client.get(url)
        self.assertEqual(AssessmentResult.objects.count(), 0)

    def test_feedback_gets_deleted(self):
        module = create_module()
        student = create_student()
        student.modules.add(module)
        performance = Performance.objects.create(
            module=module, student=student)
        assessment = Assessment.objects.create(
            module=module,
            title='Essay'
        )
        result = AssessmentResult.objects.create(assessment=assessment)
        performance.assessment_results.add(result)
        feedback = IndividualFeedback.objects.create(
            assessment_result=result,
            attempt='first'
        )
        url = (
            '/remove_student_from_module/' +
            module.code +
            '/' +
            str(module.year) +
            '/' +
            student.student_id +
            '/'
        )
        response = self.client.get(url)
        self.assertEqual(IndividualFeedback.objects.count(), 0)


class DeleteModuleTest(TeacherUnitTest):
    """Tests that the Delete Module Function removes performances and marks"""

    def test_deleting_module_deletes_everything_else(self):
        module = create_module()
        module.teachers.add(self.user.staff)
        student = create_student()
        student.modules.add(module)
        performance = Performance.objects.create(
            module=module, student=student)
        assessment = Assessment.objects.create(
            module=module,
            title="Dissertation",
            value=100,
        )
        result = AssessmentResult.objects.create(
            assessment=assessment,
            mark=60
        )
        performance.assessment_results.add(result)
        response = self.client.get(module.get_delete_self_url())
        self.assertEqual(Module.objects.count(), 0)
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(Performance.objects.count(), 0)
        self.assertEqual(Assessment.objects.count(), 0)
        self.assertEqual(AssessmentResult.objects.count(), 0)

    def test_only_instructor_or_admin_can_delete_a_module(self):
        module = create_module()
        student = create_student()
        student.modules.add(module)
        performance = Performance.objects.create(
            module=module, student=student)
        assessment = Assessment.objects.create(
            module=module,
            title="Dissertation",
            value=100,
        )
        result = AssessmentResult.objects.create(
            assessment=assessment,
            mark=60
        )
        performance.assessment_results.add(result)
        response = self.client.get(module.get_delete_self_url())
        self.assertEqual(Module.objects.count(), 1)
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(Performance.objects.count(), 1)
        self.assertEqual(Assessment.objects.count(), 1)
        self.assertEqual(AssessmentResult.objects.count(), 1)


class SeminarGroupTest(TeacherUnitTest):
    """Tests involving the seminar group setup"""

    def test_seminar_groups_can_be_saved(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student1 = stuff[1]
        student2 = stuff[2]
        student3 = stuff[3]
        request = self.factory.post(
            module.get_seminar_groups_url(),
            data={
                'action': 'Save students',
                student1.student_id: '1',
                student2.student_id: '2',
                student3.student_id: '1'
            }
        )
        request.user = self.user
        response = assign_seminar_groups(request, module.code, module.year)
        performance1 = Performance.objects.get(student=student1, module=module)
        performance2 = Performance.objects.get(student=student2, module=module)
        performance3 = Performance.objects.get(student=student3, module=module)
        self.assertEqual(performance1.seminar_group, 1)
        self.assertEqual(performance2.seminar_group, 2)
        self.assertEqual(performance3.seminar_group, 1)

    def test_seminar_groups_can_be_randomized_ignoring_previous_values(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student1 = stuff[1]
        student2 = stuff[2]
        student3 = stuff[3]
        student4 = stuff[4]
        student5 = stuff[5]
        request = self.factory.post(
            module.get_seminar_groups_url(),
            data={
                'action': 'Go',
                'ignore': True,
                'number_of_groups': '3'
            }
        )
        request.user = self.user
        response = assign_seminar_groups(request, module.code, module.year)
        performance1 = Performance.objects.get(student=student1, module=module)
        performance2 = Performance.objects.get(student=student2, module=module)
        performance3 = Performance.objects.get(student=student3, module=module)
        performance4 = Performance.objects.get(student=student4, module=module)
        performance5 = Performance.objects.get(student=student5, module=module)
        self.assertNotEqual(performance1.seminar_group, None)
        self.assertNotEqual(performance2.seminar_group, None)
        self.assertNotEqual(performance3.seminar_group, None)
        self.assertNotEqual(performance4.seminar_group, None)
        self.assertNotEqual(performance5.seminar_group, None)
        list_of_seminar_groups = []
        list_of_seminar_groups.append(performance1.seminar_group)
        list_of_seminar_groups.append(performance2.seminar_group)
        list_of_seminar_groups.append(performance3.seminar_group)
        list_of_seminar_groups.append(performance4.seminar_group)
        list_of_seminar_groups.append(performance5.seminar_group)
        self.assertTrue(1 in list_of_seminar_groups)
        self.assertTrue(2 in list_of_seminar_groups)
        self.assertTrue(3 in list_of_seminar_groups)

    def test_seminar_groups_can_be_randomized_leaving_previous_values(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student1 = stuff[1]
        performance1 = Performance.objects.get(student=student1, module=module)
        performance1.seminar_group = 1
        performance1.save()
        student2 = stuff[2]
        student3 = stuff[3]
        student4 = stuff[4]
        student5 = stuff[5]
        request = self.factory.post(
            module.get_seminar_groups_url(),
            data={
                student2.student_id: '2',
                'action': 'Go',
                'number_of_groups': '3'
            }
        )
        request.user = self.user
        response = assign_seminar_groups(request, module.code, module.year)
        performance1 = Performance.objects.get(student=student1, module=module)
        performance2 = Performance.objects.get(student=student2, module=module)
        performance3 = Performance.objects.get(student=student3, module=module)
        performance4 = Performance.objects.get(student=student4, module=module)
        performance5 = Performance.objects.get(student=student5, module=module)
        self.assertEqual(performance1.seminar_group, 1)
        self.assertEqual(performance2.seminar_group, 2)
        self.assertNotEqual(performance3.seminar_group, None)
        self.assertNotEqual(performance4.seminar_group, None)
        self.assertNotEqual(performance5.seminar_group, None)

    def test_seminar_group_overview_uses_correct_template(self):
        module = create_module()
        response = self.client.get(module.get_seminar_group_overview_url())
        self.assertTemplateUsed(response, 'seminar_group_overview.html')

    def test_seminar_group_overview_is_correct(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student1 = stuff[1]
        student2 = stuff[2]
        student3 = stuff[3]
        student4 = stuff[4]
        student5 = stuff[5]
        performance1 = Performance.objects.get(student=student1, module=module)
        performance1.seminar_group = 1
        performance1.save()
        performance2 = Performance.objects.get(student=student2, module=module)
        performance2.seminar_group = 2
        performance2.save()
        performance3 = Performance.objects.get(student=student3, module=module)
        performance3.seminar_group = 1
        performance3.save()
        performance4 = Performance.objects.get(student=student4, module=module)
        performance4.seminar_group = 2
        performance4.save()
        performance5 = Performance.objects.get(student=student5, module=module)
        performance5.seminar_group = 1
        performance5.save()
        request = self.factory.get(module.get_seminar_group_overview_url())
        request.user = self.user
        response = seminar_group_overview(request, module.code, module.year)
        soup = BeautifulSoup(response.content)
        group_1 = str(soup.select('#group_1')[0])
        group_2 = str(soup.select('#group_2')[0])
        self.assertIn(student1.short_name(), group_1)
        self.assertIn(student2.short_name(), group_2)
        self.assertIn(student3.short_name(), group_1)
        self.assertIn(student4.short_name(), group_2)
        self.assertIn(student5.short_name(), group_1)


class AssessmentTest(TeacherUnitTest):
    """Tests involving setting and deleting of assessments"""

    def test_assessments_page_uses_right_template(self):
        module = set_up_stuff()[0]
        response = self.client.get(module.get_assessment_url())
        self.assertTemplateUsed(response, 'assessment.html')

    def test_assessments_can_be_added_to_module(self):
        module = set_up_stuff()[0]
        request = self.factory.post(
            module.get_assessment_url(),
            data={
                'title': 'Hunting Exercise',
                'value': 40,
            }
        )
        request.user = self.user
        assessment(request, module.code, module.year)
        assessment_out = Assessment.objects.first()
        self.assertEqual(assessment_out.title, 'Hunting Exercise')
        self.assertEqual(assessment_out.value, 40)

    def test_assessment_can_be_deleted(self):
        stuff = set_up_stuff()
        module = stuff[0]
        performance = Performance.objects.first()
        assessment = Assessment.objects.create(
            module=module,
            title="Hunting Exercise",
            value=40
        )
        result = AssessmentResult.objects.create(
            assessment=assessment,
            mark=40
        )
        performance.assessment_results.add(result)
        self.assertEqual(Assessment.objects.count(), 1)
        self.assertEqual(AssessmentResult.objects.count(), 1)
        request = self.factory.get(assessment.get_delete_url())
        request.user = self.user
        delete_assessment(request, module.code, module.year, assessment.slug)
        self.assertEqual(Assessment.objects.count(), 0)
        self.assertEqual(AssessmentResult.objects.count(), 0)

    def test_toggle_assessment_availability_works(self):
        module = create_module()
        assessment = Assessment.objects.create(
            module=module,
            title='Hunting Exercise',
            value=100
        )
        self.assertFalse(assessment.available)
        request = self.factory.get(assessment.get_toggle_availability_url())
        request.user = self.user
        response = toggle_assessment_availability(
            request, module.code, module.year, assessment.slug, 'first')
        assessment_out = Assessment.objects.first()
        self.assertTrue(assessment_out.available)
        request = self.factory.get(assessment.get_toggle_availability_url())
        request.user = self.user
        response = toggle_assessment_availability(
            request, module.code, module.year, assessment.slug, 'first')
        assessment_out = Assessment.objects.first()
        self.assertFalse(assessment_out.available)
        request = self.factory.get(
            assessment.get_toggle_availability_url('resit'))
        request.user = self.user
        response = toggle_assessment_availability(
            request, module.code, module.year, assessment.slug, 'resit')
        assessment_out = Assessment.objects.first()
        self.assertTrue(assessment_out.resit_available)
        request = self.factory.get(
            assessment.get_toggle_availability_url('resit'))
        request.user = self.user
        response = toggle_assessment_availability(
            request, module.code, module.year, assessment.slug, 'resit')
        assessment_out = Assessment.objects.first()
        self.assertFalse(assessment_out.resit_available)
        request = self.factory.get(
            assessment.get_toggle_availability_url('second_resit'))
        request.user = self.user
        response = toggle_assessment_availability(
            request, module.code, module.year, assessment.slug, 'second_resit')
        assessment_out = Assessment.objects.first()
        self.assertTrue(assessment_out.second_resit_available)
        request = self.factory.get(
            assessment.get_toggle_availability_url('second_resit'))
        request.user = self.user
        response = toggle_assessment_availability(
            request, module.code, module.year, assessment.slug, 'second_resit')
        assessment_out = Assessment.objects.first()
        self.assertFalse(assessment_out.second_resit_available)


class AttendanceTest(TeacherUnitTest):
    """Tests around the attendance function"""

    def test_attendance_uses_correct_template(self):
        module = set_up_stuff()[0]
        response = self.client.get(module.get_attendance_url('all'))
        self.assertTemplateUsed(response, 'attendance.html')

    def test_attendance_form_shows_seminar_group(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student1 = stuff[1]
        student2 = stuff[2]
        student3 = stuff[3]
        student4 = stuff[4]
        student5 = stuff[5]
        performance1 = Performance.objects.get(student=student1, module=module)
        performance2 = Performance.objects.get(student=student2, module=module)
        performance3 = Performance.objects.get(student=student3, module=module)
        performance4 = Performance.objects.get(student=student4, module=module)
        performance5 = Performance.objects.get(student=student5, module=module)
        performance1.seminar_group = 1
        performance1.save()
        performance2.seminar_group = 1
        performance2.save()
        performance3.seminar_group = 1
        performance3.save()
        performance4.seminar_group = 2
        performance4.save()
        performance5.seminar_group = 2
        performance5.save()
        request = self.factory.get(module.get_attendance_url(1))
        request.user = self.user
        response = attendance(request, module.code, module.year, '1')
        self.assertContains(response, student1.last_name)
        self.assertContains(response, student2.last_name)
        self.assertContains(response, student3.last_name)
        self.assertNotContains(response, student4.last_name)
        self.assertNotContains(response, student5.last_name)
        request = self.factory.get(module.get_attendance_url(2))
        request.user = self.user
        response = attendance(request, module.code, module.year, '2')
        self.assertNotContains(response, student1.last_name)
        self.assertNotContains(response, student2.last_name)
        self.assertNotContains(response, student3.last_name)
        self.assertContains(response, student4.last_name)
        self.assertContains(response, student5.last_name)
        request = self.factory.get(module.get_attendance_url('all'))
        request.user = self.user
        response = attendance(request, module.code, module.year, 'all')
        self.assertContains(response, student1.last_name)
        self.assertContains(response, student2.last_name)
        self.assertContains(response, student3.last_name)
        self.assertContains(response, student4.last_name)
        self.assertContains(response, student5.last_name)

    def test_attendance_form_shows_only_active_students(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student1 = stuff[1]
        student2 = stuff[2]
        student3 = stuff[3]
        student4 = stuff[4]
        student5 = stuff[5]
        student5.active = False
        student5.save()
        performance1 = Performance.objects.get(student=student1, module=module)
        performance2 = Performance.objects.get(student=student2, module=module)
        performance3 = Performance.objects.get(student=student3, module=module)
        performance4 = Performance.objects.get(student=student4, module=module)
        performance5 = Performance.objects.get(student=student5, module=module)
        performance1.seminar_group = 1
        performance1.save()
        performance2.seminar_group = 1
        performance2.save()
        performance3.seminar_group = 1
        performance3.save()
        performance4.seminar_group = 1
        performance4.save()
        performance5.seminar_group = 1
        performance5.save()
        request = self.factory.get(module.get_attendance_url(1))
        request.user = self.user
        response = attendance(request, module.code, module.year, '1')
        self.assertContains(response, student1.last_name)
        self.assertContains(response, student2.last_name)
        self.assertContains(response, student3.last_name)
        self.assertContains(response, student4.last_name)
        self.assertNotContains(response, student5.last_name)

    def test_attendance_can_be_added_through_form(self):
        stuff = set_up_stuff()
        module = stuff[0]
        request = self.factory.post(
            module.get_attendance_url('all'),
            data={
                'bb23_1': 'p',
                'bb23_2': 'a',
                'bb23_3': 'e',
                'dd42_1': 'p',
                'dd42_3': 'a',
                'save': 'Save Changes for all weeks'
            }
        )
        request.user = self.user
        response = attendance(request, module.code, module.year, 'all')
        student1_out = Student.objects.get(student_id='bb23')
        performance1_out = Performance.objects.get(
            student=student1_out, module=module)
        student2_out = Student.objects.get(student_id='dd42')
        performance2_out = Performance.objects.get(
            student=student2_out, module=module)
        self.assertEqual(performance1_out.attendance_for(1), 'p')
        self.assertEqual(performance1_out.attendance_for(2), 'a')
        self.assertEqual(performance1_out.attendance_for(3), 'e')
        self.assertEqual(performance2_out.attendance_for(1), 'p')
        self.assertEqual(performance2_out.attendance_for(2), None)
        self.assertEqual(performance2_out.attendance_for(3), 'a')

    def test_attendance_changes_are_ignored_for_hidden_weeks(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student1 = stuff[1]
        performance1 = Performance.objects.get(student=student1, module=module)
        performance1.save_attendance('1', 'e')
        request = self.factory.post(
            module.get_attendance_url('all'),
            data={
                'bb23_1': 'p',
                'bb23_2': 'a',
                'bb23_3': 'e',
                'dd42_1': 'p',
                'dd42_3': 'a',
                'save': 'Save Changes for Week 2'
            }
        )
        request.user = self.user
        attendance(request, module.code, module.year, 'all')
        student1_out = Student.objects.get(student_id='bb23')
        performance1_out = Performance.objects.get(
            student=student1_out, module=module)
        student2_out = Student.objects.get(student_id='dd42')
        performance2_out = Performance.objects.get(
            student=student2_out, module=module)
        self.assertEqual(performance1_out.attendance_for(1), 'e')
        self.assertEqual(performance1_out.attendance_for(2), 'a')
        self.assertEqual(performance1_out.attendance_for(3), None)
        self.assertEqual(performance2_out.attendance_for(1), None)
        self.assertEqual(performance2_out.attendance_for(2), None)
        self.assertEqual(performance2_out.attendance_for(3), None)


class MarkAllAssessmentsTest(TeacherUnitTest):
    """Testing the function to mark all for one assessment openly."""

    def test_mark_all_template_is_used(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student = stuff[1]
        assessment = Assessment.objects.create(
            module=module, title="Essay", value=100)
        response = self.client.get(assessment.get_mark_all_url())
        self.assertTemplateUsed(response, 'mark_all.html')

    def test_all_students_are_shown_in_mark_all_page(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student1 = stuff[1]
        student2 = stuff[2]
        student3 = stuff[3]
        other_student = Student.objects.create(
            first_name="Road",
            last_name="Runner",
            student_id="rr42"
        )
        assessment = Assessment.objects.create(
            module=module, title="Essay", value=100)
        request = self.factory.get(assessment.get_mark_all_url())
        request.user = self.user
        response = mark_all(
            request,
            module.code,
            module.year,
            'essay',
            'first'
        )
        self.assertContains(response, student1.name())
        self.assertContains(response, student2.name())
        self.assertContains(response, student3.name())
        self.assertNotContains(response, other_student.name())

    def test_only_students_who_need_resit_show_in_mark_all_resit_page(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student1 = stuff[1]
        student2 = stuff[2]
        student3 = stuff[3]
        student4 = stuff[4]
        assessment1 = Assessment.objects.create(
            module=module, title="Essay", value=50)
        assessment2 = Assessment.objects.create(
            module=module, title="Exam", value=50)
        performance1 = Performance.objects.get(
            module=module,
            student=student1
        )
        performance2 = Performance.objects.get(
            module=module,
            student=student2
        )
        performance3 = Performance.objects.get(
            module=module,
            student=student3
        )
        performance4 = Performance.objects.get(
            module=module,
            student=student4
        )
        result_1_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=60
        )
        performance1.assessment_results.add(result_1_1)
        result_1_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=60
        )
        performance1.assessment_results.add(result_1_2)
        # Student 1 clearly passed and should not be in either
        result_2_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=30
        )
        performance2.assessment_results.add(result_2_1)
        result_2_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=30
        )
        performance2.assessment_results.add(result_2_2)
        # Student 2 clearly failed and should be in both
        result_3_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=35
        )
        performance3.assessment_results.add(result_3_1)
        result_3_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=40
        )
        performance3.assessment_results.add(result_3_2)
        # Student 3 failed (not so clearly) and should be in 1 only
        request = self.factory.get(
            assessment1.get_mark_all_url(attempt='resit')
        )
        result_4_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=60,
            concessions='G'
        )
        performance4.assessment_results.add(result_4_1)
        result_4_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=60
        )
        performance4.assessment_results.add(result_4_2)
        # Student 4 has concessions for the passed essay and should be in 1

        request.user = self.user
        response1 = mark_all(
            request,
            module.code,
            module.year,
            'essay',
            'resit'
        )
        self.assertNotContains(response1, student1.name()) 
        self.assertContains(response1, student2.name()) 
        self.assertContains(response1, student3.name()) 
        self.assertContains(response1, student4.name()) 
        request = self.factory.get(
            assessment2.get_mark_all_url(attempt='resit')
        )
        request.user = self.user
        response2 = mark_all(
            request,
            module.code,
            module.year,
            'exam',
            'resit'
        )
        self.assertNotContains(response2, student1.name()) 
        self.assertContains(response2, student2.name()) 
        self.assertNotContains(response2, student3.name()) 
        self.assertNotContains(response2, student4.name()) 

    def test_existing_results_show_up_in_mark_all_page(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student1 = stuff[1]
        assessment1 = Assessment.objects.create(
            module=module, title="Essay 1", value=50)
        assessment2 = Assessment.objects.create(
            module=module, title="Essay 2", value=50)
        performance1 = Performance.objects.get(
            module=module, student=student1)
        ar1_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=50
        )
        ar1_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=60
        )
        performance1.assessment_results.add(ar1_1)
        performance1.assessment_results.add(ar1_2)
        request = self.factory.get(assessment1.get_mark_all_url())
        request.user = self.user
        response = mark_all(
            request,
            module.code,
            module.year,
            'essay-1',
            'first'
        )
        self.assertContains(response, 60)
        html = (
            '<input class="form-control assessment_mark" type="number" ' +
            'min="0" max="100" id="essay-1_' +
            student1.student_id +
            '" name="mark_' +
            student1.student_id +
            '" type="number" value="50" /><small>Previously: 50</small>'
        )
        self.assertContains(response, html)

    def test_marks_can_be_saved_with_existing_ar_objects(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student1 = stuff[1]
        student2 = stuff[2]
        assessment1 = Assessment.objects.create(
            module=module, title="Essay 1", value=50)
        assessment2 = Assessment.objects.create(
            module=module, title="Essay 2", value=50)
        result1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=50
        )
        performance1 = Performance.objects.get(module=module, student=student1)
        performance1.assessment_results.add(result1)
        result2 = AssessmentResult.objects.create(assessment=assessment1)
        performance2 = Performance.objects.get(module=module, student=student2)
        performance2.assessment_results.add(result2)
        id1 = 'mark_' + student1.student_id
        id2 = 'mark_' + student2.student_id
        request = self.factory.post(
            assessment1.get_mark_all_url(),
            data={
                id1: '20',
                id2: '40'
            }
        )
        request.user = self.user
        response = mark_all(
            request,
            module.code,
            module.year,
            'essay-1',
            'first'
        )
        performance1_out = Performance.objects.get(
            module=module, student=student1)
        self.assertEqual(
            performance1_out.get_assessment_result('essay-1', 'first'),
            20
        )
        performance2_out = Performance.objects.get(
            module=module, student=student2)
        self.assertEqual(
            performance2_out.get_assessment_result('essay-1', 'first'),
            40
        )

    def test_marks_can_be_saved_without_existing_ar_objects(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student1 = stuff[1]
        student2 = stuff[2]
        assessment1 = Assessment.objects.create(
            module=module, title="Essay 1", value=50)
        assessment2 = Assessment.objects.create(
            module=module, title="Essay 2", value=50)
        id1 = 'mark_' + student1.student_id
        id2 = 'mark_' + student2.student_id
        request = self.factory.post(
            assessment1.get_mark_all_url(),
            data={
                id1: '20',
                id2: '40'
            }
        )
        request.user = self.user
        response = mark_all(
            request,
            module.code,
            module.year,
            'essay-1',
            'first'
        )
        performance1_out = Performance.objects.get(
            module=module, student=student1)
        self.assertEqual(
            performance1_out.get_assessment_result('essay-1', 'first'),
            20
        )
        performance2_out = Performance.objects.get(
            module=module, student=student2)
        self.assertEqual(
            performance2_out.get_assessment_result('essay-1', 'first'),
            40
        )


class MarkAllAssessmentsAnonymouslyTest(TeacherUnitTest):
    """Testing the function to mark all for one assessment anonymously."""

    def test_only_exam_ids_are_shown_if_anonymous_is_set(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student1 = stuff[1]
        student1.exam_id = '1234'
        student1.save()
        student2 = stuff[2]
        student2.exam_id = '2345'
        student2.save()
        student3 = stuff[3]
        student3.exam_id = '3456'
        student3.save()
        assessment = Assessment.objects.create(
            module=module, title="Essay", value=100)
        request = self.factory.get(assessment.get_mark_all_url(anonymous=True))
        request.user = self.user
        response = mark_all_anonymously(
            request,
            module.code,
            module.year,
            'essay',
            'first',
        )
        self.assertContains(response, student1.exam_id)
        self.assertContains(response, student2.exam_id)
        self.assertContains(response, student3.exam_id)
        self.assertNotContains(response, student1.first_name)
        self.assertNotContains(response, student1.last_name)
        self.assertNotContains(response, student1.student_id)
        self.assertNotContains(response, student2.first_name)
        self.assertNotContains(response, student2.last_name)
        self.assertNotContains(response, student2.student_id)
        self.assertNotContains(response, student3.first_name)
        self.assertNotContains(response, student3.last_name)
        self.assertNotContains(response, student3.student_id)

    def test_anonymous_marks_can_be_saved_with_existing_ar_objects(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student1 = stuff[1]
        student1.exam_id = '1234'
        student1.save()
        student2 = stuff[2]
        student2.exam_id = '2345'
        student2.save()
        assessment1 = Assessment.objects.create(
            module=module, title="Essay 1", value=50)
        assessment2 = Assessment.objects.create(
            module=module, title="Essay 2", value=50)
        result1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=50
        )
        performance1 = Performance.objects.get(module=module, student=student1)
        performance1.assessment_results.add(result1)
        result2 = AssessmentResult.objects.create(assessment=assessment1)
        performance2 = Performance.objects.get(module=module, student=student2)
        performance2.assessment_results.add(result2)
        id1 = 'mark_' + student1.exam_id
        id2 = 'mark_' + student2.exam_id
        request = self.factory.post(
            assessment1.get_mark_all_url(anonymous=True),
            data={
                id1: '20',
                id2: '40'
            }
        )
        request.user = self.user
        response = mark_all_anonymously(
            request,
            module.code,
            module.year,
            'essay-1',
            'first'
        )
        performance1_out = Performance.objects.get(
            module=module, student=student1)
        self.assertEqual(
            performance1_out.get_assessment_result('essay-1', 'first'),
            20
        )
        performance2_out = Performance.objects.get(
            module=module, student=student2)
        self.assertEqual(
            performance2_out.get_assessment_result('essay-1', 'first'),
            40
        )

    def test_anonymous_marks_can_be_saved_without_existing_ar_objects(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student1 = stuff[1]
        student1.exam_id = '1234'
        student1.save()
        student2 = stuff[2]
        student2.exam_id = '2345'
        student2.save()
        assessment1 = Assessment.objects.create(
            module=module, title="Essay 1", value=50)
        assessment2 = Assessment.objects.create(
            module=module, title="Essay 2", value=50)
        id1 = 'mark_' + student1.exam_id
        id2 = 'mark_' + student2.exam_id
        request = self.factory.post(
            assessment1.get_mark_all_url(anonymous=True),
            data={
                id1: '20',
                id2: '40'
            }
        )
        request.user = self.user
        response = mark_all_anonymously(
            request,
            module.code,
            module.year,
            'essay-1',
            'first'
        )
        performance1_out = Performance.objects.get(
            module=module, student=student1)
        self.assertEqual(
            performance1_out.get_assessment_result('essay-1', 'first'),
            20
        )
        performance2_out = Performance.objects.get(
            module=module, student=student2)
        self.assertEqual(
            performance2_out.get_assessment_result('essay-1', 'first'),
            40
        )

    def test_only_students_who_need_resit_show_in_mark_all_resit_a_page(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student1 = stuff[1]
        student1.exam_id = '1234'
        student1.save()
        student2 = stuff[2]
        student2.exam_id = '2345'
        student2.save()
        student3 = stuff[3]
        student3.exam_id = '3456'
        student3.save()
        student4 = stuff[4]
        student4.exam_id = '4567'
        student4.save()
        assessment1 = Assessment.objects.create(
            module=module, title="Essay", value=50)
        assessment2 = Assessment.objects.create(
            module=module, title="Exam", value=50)
        performance1 = Performance.objects.get(
            module=module,
            student=student1
        )
        performance2 = Performance.objects.get(
            module=module,
            student=student2
        )
        performance3 = Performance.objects.get(
            module=module,
            student=student3
        )
        performance4 = Performance.objects.get(
            module=module,
            student=student4
        )
        result_1_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=60
        )
        performance1.assessment_results.add(result_1_1)
        result_1_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=60
        )
        performance1.assessment_results.add(result_1_2)
        # Student 1 clearly passed and should not be in either
        result_2_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=30
        )
        performance2.assessment_results.add(result_2_1)
        result_2_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=30
        )
        performance2.assessment_results.add(result_2_2)
        # Student 2 clearly failed and should be in both
        result_3_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=35
        )
        performance3.assessment_results.add(result_3_1)
        result_3_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=40
        )
        performance3.assessment_results.add(result_3_2)
        # Student 3 failed (not so clearly) and should be in 1 only
        request = self.factory.get(
            assessment1.get_mark_all_url(attempt='resit')
        )
        result_4_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=60,
            concessions='G'
        )
        performance4.assessment_results.add(result_4_1)
        result_4_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=60
        )
        performance4.assessment_results.add(result_4_2)
        # Student 4 has concessions for the passed essay and should be in 1

        request.user = self.user
        request = self.factory.get(
            assessment1.get_mark_all_url(
                anonymous=True,
                attempt='resit'
            )
        )
        request.user = self.user
        response1 = mark_all_anonymously(
            request,
            module.code,
            module.year,
            'essay',
            'resit',
        )
        self.assertNotContains(response1, student1.exam_id) 
        self.assertContains(response1, student2.exam_id) 
        self.assertContains(response1, student3.exam_id) 
        self.assertContains(response1, student4.exam_id) 
        request = self.factory.get(
            assessment2.get_mark_all_url(
                anonymous=True,
                attempt='resit'
            )
        )
        request.user = self.user
        response2 = mark_all_anonymously(
            request,
            module.code,
            module.year,
            'exam',
            'resit'
        )
        self.assertNotContains(response2, student1.exam_id) 
        self.assertContains(response2, student2.exam_id) 
        self.assertNotContains(response2, student3.exam_id) 
        self.assertNotContains(response2, student4.exam_id) 


class AddEditStaffTest(AdminUnitTest):
    """Tests for adding and adding a new staff member"""

    def test_staff_can_be_added_new_user_gets_created(self):
        subject_area = SubjectArea.objects.create(name='Cartoon Studies')
        request = self.factory.post('/add_staff/', data={
            'first_name': 'Elmar',
            'last_name': 'Fudd',
            'email': 'elmar.fudd@acme.edu',
            'role': 'teacher'
        })
        request.user = self.user
        add_or_edit_staff(request, testing=True)
        user = User.objects.get(last_name='Fudd')
        staff = Staff.objects.get(user=user)
        self.assertEqual(user.staff, staff)
        self.assertEqual(user.first_name, 'Elmar')
        self.assertEqual(user.email, 'elmar.fudd@acme.edu')
        self.assertEqual(staff.role, 'teacher')

    def test_form_for_existing_staff_shows_right_details(self):
        user_in = create_user()
        subject_area = SubjectArea.objects.create(name='Cartoon Studies')
        staff_in = Staff.objects.create(user=user_in, role='teacher')
        staff_in.subject_areas.add(subject_area)
        staff_in.save()
        request = self.factory.get(staff_in.get_edit_url())
        request.user = self.user
        response = add_or_edit_staff(request, user_in.username)
        soup = BeautifulSoup(response.content)
        first_name = str(soup.select('#id_first_name')[0]['value'])
        self.assertEqual(first_name, 'Elmar')
        last_name = str(soup.select('#id_last_name')[0]['value'])
        self.assertEqual(last_name, 'Fudd')
        last_name = str(soup.select('#id_email')[0]['value'])
        self.assertEqual(last_name, 'e.fudd@acme.edu')
        teacher_option = str(soup.find(value='teacher'))
        self.assertTrue('selected="selected"' in teacher_option)

    def test_staff_member_can_be_edited(self):
        user_in = User.objects.create_user(
            'ef10', 'e.fudd@acme.edu', 'rabbitseason')
        user_in.last_name = 'Fadd'
        user_in.first_name = 'Elmar'
        user_in.save()
        subject_area = SubjectArea.objects.create(name='Cartoon Studies')
        staff_in = Staff.objects.create(user=user_in, role='teacher')
        staff_in.subject_areas.add(subject_area)
        staff_in.save()
        request = self.factory.post(staff_in.get_edit_url(), data={
            'first_name': 'Elmar',
            'last_name': 'Fudd',
            'email': 'elmar.fudd@acme.edu',
            'role': 'admin'
        })
        request.user = self.user
        add_or_edit_staff(request, user_in.username, testing=True)
        staff_out = Staff.objects.get(user=user_in)
        self.assertEqual(staff_out.user.last_name, 'Fudd')
        self.assertEqual(staff_out.role, 'admin')


class ViewStaffTest(AdminUnitTest):
    """Tests for Viewing Staff Members"""

    def test_staff_view_by_subject_uses_correct_template(self):
        response = self.client.get('/view_staff_by_subject/')
        self.assertTemplateUsed(response, 'all_staff_by_subject.html')

    def test_staff_view_by_subject_contains_staff(self):
        subject_area_1 = create_subject_area()
        subject_area_2 = SubjectArea.objects.create(name='Evil Plotting')
        staff1 = create_teacher()
        staff1.subject_areas.add(subject_area_1)
        staff1.save()
        user2 = User.objects.create_user(
            'ys142', 'y.sam@acme.edu', 'squaredance')
        user2.last_name = 'Sam'
        user2.first_name = 'Yosemite'
        user2.save()
        staff2 = Staff.objects.create(user=user2, role='Teacher')
        staff2.subject_areas.add(subject_area_1)
        staff2.subject_areas.add(subject_area_2)
        staff2.save()
        user3 = User.objects.create_user(
            'ta123', 't.avery@acme.edu', 'othergod')
        user3.first_name = 'Tex'
        user3.last_name = 'Avery'
        user3.save()
        staff3 = Staff.objects.create(user=user3, role='Admin')
        staff3.subject_areas.add(subject_area_1)
        staff3.save()
        request = self.factory.get('/view_staff_by_subject/')
        request.user = self.user
        response = view_staff_by_subject(request)
        soup = BeautifulSoup(response.content)
        table1 = str(soup.find(id=subject_area_1.slug))
        self.assertTrue(staff1.name() in table1)
        self.assertTrue(staff2.name() in table1)
        self.assertTrue(staff3.name() in table1)
        table2 = str(soup.find(id=subject_area_2.slug))
        self.assertFalse(staff1.name() in table2)
        self.assertTrue(staff2.name() in table2)
        self.assertFalse(staff3.name() in table2)

    def test_staff_view_by_name_contains_staff(self):
        subject_area_1 = create_subject_area()
        subject_area_2 = SubjectArea.objects.create(name='Evil Plotting')
        staff1 = create_teacher()
        staff1.subject_areas.add(subject_area_1)
        staff1.save()
        user2 = User.objects.create_user(
            'ys142', 'y.sam@acme.edu', 'squaredance')
        user2.last_name = 'Sam'
        user2.first_name = 'Yosemite'
        user2.save()
        staff2 = Staff.objects.create(user=user2, role='Teacher')
        staff2.subject_areas.add(subject_area_1)
        staff2.subject_areas.add(subject_area_2)
        staff2.save()
        user3 = User.objects.create_user(
            'ta142', 't.avery@acme.edu', 'othergod')
        user3.first_name = 'Tex'
        user3.last_name = 'Avery'
        user3.save()
        staff3 = Staff.objects.create(user=user3, role='Admin')
        staff3.subject_areas.add(subject_area_1)
        staff3.save()
        request = self.factory.get('/view_staff_by_name/')
        request.user = self.user
        response = view_staff_by_name(request)
        self.assertContains(response, staff1.name())
        self.assertContains(response, staff2.name())
        self.assertContains(response, staff3.name())


class YearViewTest(AdminUnitTest):
    """Tests around the year view function from a teacher's perspective"""

    def test_year_view_uses_right_template(self):
        response = self.client.get('/students/all/')
        self.assertTemplateUsed(response, 'year_view.html')

    def test_teachers_see_all_students_from_their_only_subject_area(self):
        stuff = set_up_stuff()
        subject_area1 = SubjectArea.objects.create(name="Cartoon Studies")
        subject_area2 = SubjectArea.objects.create(name="Evil Plotting")
        self.user.staff.subject_areas.add(subject_area1)
        course1 = Course.objects.create(
            title="BA in Cartoon Studies", short_title="Cartoon Studies")
        course1.subject_areas.add(subject_area1)
        course2 = Course.objects.create(
            title="BA in Evil Plotting", short_title="Evil Plotting")
        course2.subject_areas.add(subject_area2)
        course3 = Course.objects.create(
            title="BA in Cartoon Studies with Evil Plotting",
            short_title="Cartoon Studies / Evil Plotting"
        )
        course3.subject_areas.add(subject_area1)
        course3.subject_areas.add(subject_area2)
        student1 = stuff[1]
        student1.year = 1
        student1.course = course1
        student1.save()
        student2 = stuff[2]
        student2.year = 1
        student2.course = course1
        student2.save()
        student3 = stuff[3]
        student3.course = course2
        student3.year = 1
        student3.save()
        student4 = stuff[4]
        student4.course = course3
        student4.year = 1
        student4.save()
        request = self.factory.get('/year_view/1/')
        request.user = self.user
        response = year_view(request, '1')
        self.assertContains(response, student1.last_name)
        self.assertContains(response, student2.last_name)
        self.assertNotContains(response, student3.last_name)
        self.assertContains(response, student4.last_name)

    def test_teachers_see_all_students_from_their_many_subject_areas(self):
        stuff = set_up_stuff()
        subject_area1 = SubjectArea.objects.create(name="Cartoon Studies")
        subject_area2 = SubjectArea.objects.create(name="Evil Plotting")
        self.user.staff.subject_areas.add(subject_area1)
        self.user.staff.subject_areas.add(subject_area2)
        course1 = Course.objects.create(
            title="BA in Cartoon Studies", short_title="Cartoon Studies")
        course1.subject_areas.add(subject_area1)
        course2 = Course.objects.create(
            title="BA in Evil Plotting", short_title="Evil Plotting")
        course2.subject_areas.add(subject_area2)
        course3 = Course.objects.create(
            title="BA in Cartoon Studies with Evil Plotting",
            short_title="Cartoon Studies / Evil Plotting"
        )
        course3.subject_areas.add(subject_area1)
        course3.subject_areas.add(subject_area2)
        student1 = stuff[1]
        student1.year = 1
        student1.course = course1
        student1.save()
        student2 = stuff[2]
        student2.year = 1
        student2.course = course1
        student2.save()
        student3 = stuff[3]
        student3.course = course2
        student3.year = 1
        student3.save()
        student4 = stuff[4]
        student4.course = course3
        student4.year = 1
        student4.save()
        request = self.factory.get('/year_view/1/')
        request.user = self.user
        response = year_view(request, '1')
        self.assertContains(response, student1.last_name)
        self.assertContains(response, student2.last_name)
        self.assertContains(response, student3.last_name)
        self.assertContains(response, student4.last_name)

    def test_main_admin_sees_all_active_students_for_a_year_are_shown(self):
        stuff = set_up_stuff()
        self.user.staff.main_admin = True
        self.user.staff.save()
        student1 = stuff[1]
        student2 = stuff[2]
        student3 = stuff[3]
        student4 = stuff[4]
        student4.year = 2
        student4.save()
        student5 = stuff[5]
        student5.active = False
        student5.save()
        request = self.factory.get('/year_view/1/')
        request.user = self.user
        response = year_view(request, '1')
        self.assertContains(response, student1.last_name)
        self.assertContains(response, student2.last_name)
        self.assertContains(response, student3.last_name)
        self.assertNotContains(response, student4.last_name)
        self.assertNotContains(response, student5.last_name)

    def test_only_admin_and_programme_director_see_edit_stuff(self):
        stuff = set_up_stuff()
        subject_area = create_subject_area()
        course = create_course()
        course.subject_areas.add(subject_area)
        self.user.staff.role = 'admin'
        self.user.staff.subject_areas.add(subject_area)
        self.user.staff.save()
        student1 = stuff[1]
        student1.course = course
        student1.save()
        student2 = stuff[2]
        student2.course = course
        student2.save()
        request = self.factory.get('/year_view/1/')
        request.user = self.user
        response = year_view(request, '1')
        self.assertContains(response, 'bulkfunctions')
        self.user.staff.role = 'teacher'
        self.user.staff.save()
        request = self.factory.get('/year_view/1/')
        request.user = self.user
        response = year_view(request, '1')
        self.assertNotContains(response, 'bulkfunctions')
        self.user.staff.role = 'teacher'
        self.user.staff.programme_director = True
        self.user.staff.save()
        request = self.factory.get('/year_view/1/')
        request.user = self.user
        response = year_view(request, '1')
        self.assertContains(response, 'bulkfunctions')

    def test_bulk_changing_functions_work(self):
        stuff = set_up_stuff()
        subject_area = create_subject_area()
        course1 = create_course()
        course1.subject_areas.add(subject_area)
        course2 = Course.objects.create(
            title='BA in Evil Plotting', short_title='Evil Plotting')
        subject_area2 = SubjectArea.objects.create(name='Evil Plotting')
        course2.subject_areas.add(subject_area2)
        self.user.staff.role = 'admin'
        self.user.staff.subject_areas.add(subject_area)
        self.user.staff.save()
        student1 = stuff[1]
        student1.course = course1
        student1.qld = True
        student1.save()
        student2 = stuff[2]
        student2.course = course1
        student2.qld = True
        student2.save()
        student3 = stuff[3]
        student3.course = course1
        student3.qld = True
        student3.save()
        stuff[4].delete()
        stuff[5].delete()
        # Set course
        request = self.factory.post('/year_view/1/', data={
            'selected_student_id': [student2.student_id, student3.student_id],
            'modify': 'course_BA in Evil Plotting'
        })
        request.user = self.user
        response = year_view(request, '1')
        student1_out = Student.objects.get(student_id=student1.student_id)
        student2_out = Student.objects.get(student_id=student2.student_id)
        student3_out = Student.objects.get(student_id=student3.student_id)
        self.assertEqual(student1_out.course, course1)
        self.assertEqual(student2_out.course, course2)
        self.assertEqual(student3_out.course, course2)
        # Set QLD
        request = self.factory.post('/year_view/1/', data={
            'selected_student_id': [student1.student_id, student2.student_id],
            'modify': 'qld_off'
        })
        request.user = self.user
        response = year_view(request, '1')
        student1_out = Student.objects.get(student_id=student1.student_id)
        student2_out = Student.objects.get(student_id=student2.student_id)
        student3_out = Student.objects.get(student_id=student3.student_id)
        self.assertEqual(student1_out.qld, False)
        self.assertEqual(student2_out.qld, False)
        self.assertEqual(student3_out.qld, True)
        # Set begin of studies
        request = self.factory.post('/year_view/1/', data={
            'selected_student_id': [student1.student_id, student2.student_id],
            'modify': 'since_1900'
        })
        request.user = self.user
        response = year_view(request, '1')
        student1_out = Student.objects.get(student_id=student1.student_id)
        student2_out = Student.objects.get(student_id=student2.student_id)
        student3_out = Student.objects.get(student_id=student3.student_id)
        self.assertEqual(student1_out.since, 1900)
        self.assertEqual(student2_out.since, 1900)
        self.assertEqual(student3_out.since, None)
        # Set Year
        request = self.factory.post('/year_view/1/', data={
            'selected_student_id': [student1.student_id, student2.student_id],
            'modify': 'year_2'
        })
        request.user = self.user
        response = year_view(request, '1')
        student1_out = Student.objects.get(student_id=student1.student_id)
        student2_out = Student.objects.get(student_id=student2.student_id)
        student3_out = Student.objects.get(student_id=student3.student_id)
        self.assertEqual(student1_out.year, 2)
        self.assertEqual(student2_out.year, 2)
        self.assertEqual(student3_out.year, 1)
        # Active
        request = self.factory.post('/year_view/1/', data={
            'selected_student_id': [student1.student_id, student2.student_id],
            'modify': 'active_no'
        })
        request.user = self.user
        response = year_view(request, '1')
        student1_out = Student.objects.get(student_id=student1.student_id)
        student2_out = Student.objects.get(student_id=student2.student_id)
        student3_out = Student.objects.get(student_id=student3.student_id)
        self.assertEqual(student1_out.active, False)
        self.assertEqual(student2_out.active, False)
        self.assertEqual(student3_out.active, True)
        # Delete
        request = self.factory.post('/year_view/1/', data={
            'selected_student_id': [student1.student_id, student2.student_id],
            'modify': 'delete_yes'
        })
        request.user = self.user
        response = year_view(request, '1')
        self.assertEqual(Student.objects.count(), 1)

    def test_deleting_student_deletes_everything(self):
        module = create_module()
        student = create_student()
        student.modules.add(module)
        performance = Performance.objects.create(
            module=module, student=student)
        assessment = Assessment.objects.create(
            module=module,
            title='Essay'
        )
        result = AssessmentResult.objects.create(assessment=assessment)
        feedback = IndividualFeedback.objects.create(
            assessment_result=result,
            attempt='first'
        )
        self.assertEqual(AssessmentResult.objects.count(), 1)
        self.assertEqual(IndividualFeedback.objects.count(), 1)
        performance.assessment_results.add(result)
        request = self.factory.post('/year_view/1/', data={
            'selected_student_id': [student.student_id],
            'modify': 'delete_yes'
        })
        request.user = self.user
        response = year_view(request, '1')
        self.assertEqual(AssessmentResult.objects.count(), 0)
        self.assertEqual(IndividualFeedback.objects.count(), 0)


class CSVParsingTests(AdminUnitTest):
    """Tests for the CSV Parsing"""

    def test_csv_data_gets_parsed_properly(self):
        parsed_csvlist = (
            'bb42;Bunny;Bugs;1900;1;bb42@acme.edu;+112345678/////' +
            'dd23;Duck;Daffy;1900;1;dd23@acme.edu;+123456789/////' +
            'pp42;Pig;Porky;1899;2;pp42@acme.edu;+134567890/////' +
            'test;wrong;entry;to;beignored'
        )
        data = Data.objects.create(id='randomstring', value=parsed_csvlist)
        request = self.factory.post('/parse_csv/randomstring/', data={
            'column1': 'student_id',
            'column2': 'last_name',
            'column3': 'first_name',
            'column4': 'since',
            'column5': 'year',
            'column6': 'email',
            'column7': 'phone_number',
            'exclude': '4'
        })
        request.user = self.user
        parse_csv(request, data.id)
        self.assertEqual(Student.objects.count(), 3)
        student1 = Student.objects.get(student_id='bb42')
        student2 = Student.objects.get(student_id='dd23')
        student3 = Student.objects.get(student_id='pp42')
        self.assertEqual(student1.last_name, 'Bunny')
        self.assertEqual(student1.first_name, 'Bugs')
        self.assertEqual(student1.since, 1900)
        self.assertEqual(student1.email, 'bb42@acme.edu')
        self.assertEqual(student1.phone_number, '+112345678')


class AssignTutorsTest(AdminUnitTest):
    """Tests for the assigning tutors view from an admin perspective"""

    def test_right_template_used(self):
        SubjectArea.objects.create(name="Cartoon Studies")
        response = self.client.get('/assign_tutors/cartoon-studies/1/')
        self.assertTemplateUsed(response, 'assign_tutors.html')

    def test_assign_tutors_view_shows_right_tutors(self):
        subject_area1 = SubjectArea.objects.create(name="Cartoon Studies")
        subject_area2 = SubjectArea.objects.create(name="Evil Plotting")
        user1 = User.objects.create_user(
            username='ef1',
            password='rabbitseason',
            last_name='Fudd',
            first_name='Elmar'
        )
        staff1 = Staff.objects.create(user=user1, role='teacher')
        staff1.subject_areas.add(subject_area1)
        user2 = User.objects.create_user(
            username='ys2',
            password='squaredance',
            last_name='Sam',
            first_name='Yosemite'
        )
        staff2 = Staff.objects.create(user=user2, role='teacher')
        staff2.subject_areas.add(subject_area2)
        user3 = User.objects.create_user(
            username='mtm3',
            password='zapp',
            last_name='The Martian',
            first_name='Marvin'
        )
        staff3 = Staff.objects.create(user=user3, role='teacher')
        staff3.subject_areas.add(subject_area1)
        staff3.subject_areas.add(subject_area2)
        request = self.factory.get('/assign_tutors/cartoon-studies/1')
        request.user = self.user
        response = assign_tutors(request, 'cartoon-studies', '1')
        soup = BeautifulSoup(response.content)
        table = str(soup.select('#teachers')[0])
        self.assertTrue(user1.last_name in table)
        self.assertFalse(user2.last_name in table)
        self.assertTrue(user3.last_name in table)

    def test_assign_tutors_view_shows_right_students(self):
        subject_area1 = SubjectArea.objects.create(name="Cartoon Studies")
        subject_area2 = SubjectArea.objects.create(name="Evil Plotting")
        course1 = Course.objects.create(title='BA in Cartoon Studies')
        course1.subject_areas.add(subject_area1)
        course2 = Course.objects.create(title='BA in Evil Plotting')
        course2.subject_areas.add(subject_area2)
        course3 = Course.objects.create(
            title='BA in Cartoon Studies with Evil Plotting')
        course3.subject_areas.add(subject_area1, subject_area2)
        user1 = User.objects.create_user(
            username='ef1',
            password='rabbitseason',
            last_name='Fudd',
            first_name='Elmar'
        )
        staff1 = Staff.objects.create(user=user1, role='teacher')
        staff1.subject_areas.add(subject_area1)
        student1 = Student.objects.create(
            student_id='bb42',
            first_name='Bugs',
            last_name='Bunny',
            course=course1,
            year=1
        )
        student2 = Student.objects.create(
            student_id='dd23',
            first_name='Duck',
            last_name='Daffy',
            course=course2,
            year=1
        )
        student3 = Student.objects.create(
            student_id='pp23',
            first_name='Porky',
            last_name='Pig',
            course=course3,
            year=1
        )
        student4 = Student.objects.create(
            student_id='rr23',
            first_name='Road',
            last_name='Runner',
            course=course1,
            year=2
        )
        request = self.factory.get('/assign_tutors/cartoon-studies/1')
        request.user = self.user
        response = assign_tutors(request, 'cartoon-studies', '1')
        self.assertContains(response, 'Bunny')
        self.assertNotContains(response, 'Duck')
        self.assertContains(response, 'Pig')
        self.assertNotContains(response, 'Runner')

    def test_tutors_can_be_assigned(self):
        subject_area = SubjectArea.objects.create(name="Cartoon Studies")
        course = Course.objects.create(title='BA in Cartoon Studies')
        course.subject_areas.add(subject_area)
        user1 = User.objects.create_user(
            username='ef1',
            password='rabbitseason',
            last_name='Fudd',
            first_name='Elmar'
        )
        staff1 = Staff.objects.create(user=user1, role='teacher')
        staff1.subject_areas.add(subject_area)
        user2 = User.objects.create_user(
            username='ys2',
            password='squaredance',
            last_name='Sam',
            first_name='Yosemite'
        )
        staff2 = Staff.objects.create(user=user2, role='teacher')
        staff2.subject_areas.add(subject_area)
        student1 = Student.objects.create(
            student_id='bb42',
            first_name='Bugs',
            last_name='Bunny',
            course=course,
            year=1
        )
        student2 = Student.objects.create(
            student_id='dd23',
            first_name='Duck',
            last_name='Daffy',
            course=course,
            year=1
        )
        student3 = Student.objects.create(
            student_id='pp23',
            first_name='Porky',
            last_name='Pig',
            course=course,
            year=1
        )
        student4 = Student.objects.create(
            student_id='rr23',
            first_name='Road',
            last_name='Runner',
            course=course,
            year=1
        )
        request = self.factory.post(
            '/assign_tutors/cartoon-studies/1',
            data={
                'bb42': 'ef1',
                'dd23': 'ys2',
                'pp23': 'ef1'
            }
        )
        request.user = self.user
        response = assign_tutors(request, 'cartoon-studies', '1')
        student1_out = Student.objects.get(student_id='bb42')
        self.assertEqual(student1_out.tutor, staff1)
        student2_out = Student.objects.get(student_id='dd23')
        self.assertEqual(student2_out.tutor, staff2)
        student3_out = Student.objects.get(student_id='pp23')
        self.assertEqual(student3_out.tutor, staff1)
        student4_out = Student.objects.get(student_id='rr23')
        self.assertEqual(student4_out.tutor, None)


class AllTuteeMeetingTest(TeacherUnitTest):
    """Tests about the function showing all tutee meetings"""

    def test_page_can_only_be_seen_by_pd(self):
        subject_area = create_subject_area()
        url = (
            '/all_tutee_meetings/' +
            subject_area.slug +
            '/1/'
        )
        request = self.factory.get(url)
        request.user = self.user
        response = all_tutee_meetings(request, 'cartoon-studies', '1')
        self.assertNotEqual(response.status_code, 200)
        self.user.staff.programme_director = True
        self.user.staff.save()
        request = self.factory.get(url)
        request.user = self.user
        response = all_tutee_meetings(request, 'cartoon-studies', '1')
        self.assertEqual(response.status_code, 200)

    def test_page_uses_right_template(self):
        subject_area = create_subject_area()
        url = (
            '/all_tutee_meetings/' +
            subject_area.slug +
            '/1/'
        )
        self.user.staff.programme_director = True
        self.user.staff.save()
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'all_tutees.html')

    def test_students_in_the_right_year_show_up(self):
        subject_area = create_subject_area()
        course = Course.objects.create(title='Cartoon Studies')
        course.subject_areas.add(subject_area)
        student1 = Student.objects.create(
            student_id='bb1',
            first_name='Bugs',
            last_name='Bunny',
            year=1,
            course=course
        )
        student2 = Student.objects.create(
            student_id='dd1',
            first_name='Duck',
            last_name='Daffy',
            year=2,
            course=course
        )
        url = (
            '/all_tutee_meetings/' +
            subject_area.slug +
            '/1/'
        )
        self.user.staff.programme_director = True
        self.user.staff.save()
        request = self.factory.get(url)
        request.user = self.user
        response = all_tutee_meetings(request, 'cartoon-studies', '1')
        self.assertContains(response, student1.get_absolute_url())
        self.assertNotContains(response, student2.get_absolute_url())

    def test_tutor_appears_on_page(self):
        subject_area = create_subject_area()
        course = Course.objects.create(title='Cartoon Studies')
        course.subject_areas.add(subject_area)
        teacher = create_teacher()
        student1 = Student.objects.create(
            student_id='bb1',
            first_name='Bugs',
            last_name='Bunny',
            year=1,
            course=course,
            tutor=teacher
        )
        url = (
            '/all_tutee_meetings/' +
            subject_area.slug +
            '/1/'
        )
        self.user.staff.programme_director = True
        self.user.staff.save()
        request = self.factory.get(url)
        request.user = self.user
        response = all_tutee_meetings(request, 'cartoon-studies', '1')
        self.assertContains(response, student1.get_absolute_url())
        self.assertContains(response, teacher.name())

    def test_tutor_meetings_appear(self):
        subject_area = create_subject_area()
        course = Course.objects.create(title='Cartoon Studies')
        course.subject_areas.add(subject_area)
        teacher = create_teacher()
        student1 = Student.objects.create(
            student_id='bb1',
            first_name='Bugs',
            last_name='Bunny',
            year=1,
            course=course,
            tutor=teacher
        )
        student2 = Student.objects.create(
            student_id='dd1',
            first_name='Duck',
            last_name='Daffy',
            year=1,
            course=course,
            tutor=teacher
        )
        date = datetime.date(1900, 1, 1)
        meeting1 = TuteeSession.objects.create(
            tutor=teacher,
            tutee=student1,
            date_of_meet=date,
            notes="Some Text"
        )
        url = (
            '/all_tutee_meetings/' +
            subject_area.slug +
            '/1/'
        )
        self.user.staff.programme_director = True
        self.user.staff.save()
        request = self.factory.get(url)
        request.user = self.user
        response = all_tutee_meetings(request, 'cartoon-studies', '1')
        self.assertContains(response, '1 Jan 1900')
        self.assertContains(response, meeting1.get_absolute_url())


class MyTuteesTests(TeacherUnitTest):
    """Making sure that the my tutee view shows everything necessary"""

    def test_all_tutees_are_shown(self):
        stuff = set_up_stuff()
        student1 = stuff[1]
        student2 = stuff[2]
        student3 = stuff[3]
        student4 = stuff[4]
        student5 = stuff[5]
        student1.tutor = self.user.staff
        student1.save()
        student2.tutor = self.user.staff
        student2.save()
        student3.tutor = self.user.staff
        student3.save()
        request = self.factory.get('/my_tutees/')
        request.user = self.user
        response = my_tutees(request)
        self.assertContains(response, student1.name())
        self.assertContains(response, student2.name())
        self.assertContains(response, student3.name())
        self.assertNotContains(response, student4.name())
        self.assertNotContains(response, student5.name())

    def test_all_tutee_meetings_are_shown(self):
        student = create_student()
        student.tutor = self.user.staff
        student.save()
        date1 = datetime.date(1900, 1, 1)
        date2 = datetime.date(1900, 1, 2)
        meeting1 = TuteeSession.objects.create(
            tutor=self.user.staff,
            tutee=student,
            date_of_meet=date1,
            notes='Text'
        )
        meeting2 = TuteeSession.objects.create(
            tutor=self.user.staff,
            tutee=student,
            date_of_meet=date2,
            notes='Text'
        )
        request = self.factory.get('/my_tutees/')
        request.user = self.user
        response = my_tutees(request)
        self.assertContains(response, '1 Jan 1900')
        self.assertContains(response, '2 Jan 1900')


class AddressNinesTest(TeacherUnitTest):
    """Tests the function that allows to change averages ending with 9"""

    def test_address_nines_uses_right_template(self):
        module = create_module()
        response = self.client.get(module.get_address_nines_url())
        self.assertTemplateUsed(response, 'address_nines.html')

    def test_address_nines_shows_all_averages_ending_with_nine(self):
        stuff = set_up_stuff()
        module = stuff[0]
        assessment1 = Assessment.objects.create(
            module=module,
            title='Assessment 1',
            value=20
        )
        assessment2 = Assessment.objects.create(
            module=module,
            title='Assessment 2',
            value=30
        )
        assessment3 = Assessment.objects.create(
            module=module,
            title='Assessment 3',
            value=50
        )
        # Student 1 with average of 49
        student1 = stuff[1]
        performance1 = Performance.objects.get(module=module, student=student1)
        result1_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=50
        )
        performance1.assessment_results.add(result1_1)
        result1_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=48
        )
        performance1.assessment_results.add(result1_2)
        result1_3 = AssessmentResult.objects.create(
            assessment=assessment3,
            mark=50
        )
        performance1.assessment_results.add(result1_3)
        performance1.calculate_average()
        # Student 2 with 59 Average
        student2 = stuff[2]
        performance2 = Performance.objects.get(module=module, student=student2)
        result2_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=62
        )
        performance2.assessment_results.add(result2_1)
        result2_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=58
        )
        performance2.assessment_results.add(result2_2)
        result2_3 = AssessmentResult.objects.create(
            assessment=assessment3,
            mark=59
        )
        performance2.assessment_results.add(result2_3)
        performance2.calculate_average()
        # Student 3 with 60 Average
        student3 = stuff[3]
        performance3 = Performance.objects.get(module=module, student=student3)
        result3_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=60
        )
        performance3.assessment_results.add(result3_1)
        result3_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=60
        )
        performance3.assessment_results.add(result3_2)
        result3_3 = AssessmentResult.objects.create(
            assessment=assessment3,
            mark=60
        )
        performance3.assessment_results.add(result3_3)
        performance3.calculate_average()
        request = self.factory.get(module.get_address_nines_url())
        request.user = self.user
        response = address_nines(request, module.code, module.year)
        self.assertContains(response, student1.short_name())
        self.assertContains(response, student2.short_name())
        self.assertNotContains(response, student3.short_name())

    def test_address_nines_shows_no_nines_found_message_when_no_nines(self):
        stuff = set_up_stuff()
        module = stuff[0]
        assessment1 = Assessment.objects.create(
            module=module,
            title='Assessment 1',
            value=20
        )
        assessment2 = Assessment.objects.create(
            module=module,
            title='Assessment 2',
            value=30
        )
        assessment3 = Assessment.objects.create(
            module=module,
            title='Assessment 3',
            value=50
        )
        # Student 1 with 40 average
        student1 = stuff[1]
        performance1 = Performance.objects.get(module=module, student=student1)
        result1_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=40
        )
        performance1.assessment_results.add(result1_1)
        result1_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=40
        )
        performance1.assessment_results.add(result1_2)
        result1_3 = AssessmentResult.objects.create(
            assessment=assessment3,
            mark=40
        )
        performance1.assessment_results.add(result1_3)
        performance1.calculate_average()
        # Student 2 with 55 Average
        student2 = stuff[2]
        performance2 = Performance.objects.get(module=module, student=student2)
        result2_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=55
        )
        performance2.assessment_results.add(result2_1)
        result2_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=55
        )
        performance2.assessment_results.add(result2_2)
        result2_3 = AssessmentResult.objects.create(
            assessment=assessment3,
            mark=55
        )
        performance2.assessment_results.add(result2_3)
        performance2.calculate_average()
        # Student 3 with 60 Average
        student3 = stuff[3]
        performance3 = Performance.objects.get(module=module, student=student3)
        result3_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=60
        )
        performance3.assessment_results.add(result3_1)
        result3_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=60
        )
        performance3.assessment_results.add(result3_2)
        result3_3 = AssessmentResult.objects.create(
            assessment=assessment3,
            mark=60
        )
        performance3.assessment_results.add(result3_3)
        performance3.calculate_average()
        request = self.factory.get(module.get_address_nines_url())
        request.user = self.user
        response = address_nines(request, module.code, module.year)
        self.assertNotContains(response, student1.short_name())
        self.assertNotContains(response, student2.short_name())
        self.assertNotContains(response, student3.short_name())
        self.assertContains(response, 'no averages ending with a 9')

    def test_address_nines_changes_marks(self):
        stuff = set_up_stuff()
        module = stuff[0]
        assessment1 = Assessment.objects.create(
            module=module,
            title='Assessment 1',
            value=20
        )
        assessment2 = Assessment.objects.create(
            module=module,
            title='Assessment 2',
            value=30
        )
        assessment3 = Assessment.objects.create(
            module=module,
            title='Assessment 3',
            value=50
        )
        # Student 1 with average of 49
        student1 = stuff[1]
        performance1 = Performance.objects.get(module=module, student=student1)
        result1_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=50
        )
        r1_1_field = 'mark_' + assessment1.slug + '_' + student1.student_id
        performance1.assessment_results.add(result1_1)
        result1_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=48
        )
        performance1.assessment_results.add(result1_2)
        r1_2_field = 'mark_' + assessment2.slug + '_' + student1.student_id 
        result1_3 = AssessmentResult.objects.create(
            assessment=assessment3,
            mark=50
        )
        performance1.assessment_results.add(result1_3)
        r1_3_field = 'mark_' + assessment3.slug + '_' + student1.student_id 
        performance1.calculate_average()
        # Student 2 with 59 Average
        student2 = stuff[2]
        performance2 = Performance.objects.get(module=module, student=student2)
        result2_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=62
        )
        performance2.assessment_results.add(result2_1)
        r2_1_field = 'mark_' + assessment1.slug + '_' + student2.student_id 
        result2_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=58
        )
        performance2.assessment_results.add(result2_2)
        r2_2_field = 'mark_' + assessment2.slug + '_' + student2.student_id 
        result2_3 = AssessmentResult.objects.create(
            assessment=assessment3,
            mark=59
        )
        performance2.assessment_results.add(result2_3)
        r2_3_field = 'mark_' + assessment3.slug + '_' + student2.student_id 
        performance2.calculate_average()
        request = self.factory.post(
            module.get_address_nines_url(),
            data={
                r1_1_field: '50',
                r1_2_field: '49',
                r1_3_field: '50',
                r2_1_field: '63',
                r2_2_field: '58',
                r2_3_field: '59'
            }
        )
        request.user = self.user
        response = address_nines(request, module.code, module.year)
        performance_1_out = Performance.objects.get(
            student=student1, module=module
        )
        performance_2_out = Performance.objects.get(
            student=student2, module=module
        )
        self.assertEqual(performance_1_out.average, 50)
        self.assertEqual(performance_2_out.average, 60)

    def test_address_nines_templates_contains_correct_form_tags(self):
        stuff = set_up_stuff()
        module = stuff[0]
        assessment1 = Assessment.objects.create(
            module=module,
            title='Assessment 1',
            value=20
        )
        assessment2 = Assessment.objects.create(
            module=module,
            title='Assessment 2',
            value=30
        )
        assessment3 = Assessment.objects.create(
            module=module,
            title='Assessment 3',
            value=50
        )
        # Student 1 with average of 49
        student1 = stuff[1]
        performance1 = Performance.objects.get(module=module, student=student1)
        result1_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=50
        )
        r1_1_field = (
            'name="mark_' +
            assessment1.slug + 
            '_' +
            student1.student_id +
            '"'
        )
        performance1.assessment_results.add(result1_1)
        result1_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=48
        )
        r1_2_field = (
            'name="mark_' +
            assessment2.slug + 
            '_' +
            student1.student_id +
            '"'
        )
        performance1.assessment_results.add(result1_2)
        result1_3 = AssessmentResult.objects.create(
            assessment=assessment3,
            mark=50
        )
        r1_3_field = (
            'name="mark_' +
            assessment3.slug + 
            '_' +
            student1.student_id +
            '"'
        )
        performance1.assessment_results.add(result1_3)
        performance1.calculate_average()
        request = self.factory.get(module.get_address_nines_url())
        request.user = self.user
        response = address_nines(request, module.code, module.year)
        self.assertContains(response, r1_1_field)
        self.assertContains(response, r1_2_field)
        self.assertContains(response, r1_3_field)


class EditExamIDsTest(AdminUnitTest):
    """Testing the function to manually edit Exam IDs"""

    def test_right_template_used(self):
        subject_area = SubjectArea.objects.create(name="Cartoon Studies")
        url = (
            '/edit_exam_ids/' +
            subject_area.slug +
            '/1/'
        )
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'edit_exam_ids.html')
    
    def test_only_active_students_with_right_SA_and_year_appear_in_form(self):
        subject_area1 = SubjectArea.objects.create(name="Cartoon Studies")
        subject_area2 = SubjectArea.objects.create(name="Evil Plotting")
        course1 = Course.objects.create(
            title="MA in Cartoon Studies",
            short_title="Cartoon Studies"
        )
        course1.subject_areas.add(subject_area1)
        course2 = Course.objects.create(
            title="MSc in Evil Plotting",
            short_title="Evil Plotting"
        )
        course2.subject_areas.add(subject_area2)
        course3 = Course.objects.create(
            title="MA in Cartoon Studies and Evil Plotting",
            short_title="Cartoon Studies/Evil Plotting"
        )
        course3.subject_areas.add(subject_area1)
        course3.subject_areas.add(subject_area2)
        stuff = set_up_stuff()
        student1 = stuff[1]
        student1.active = True
        student1.course = course1
        student1.year = 1
        student1.save()
        student2 = stuff[2]
        student2.active = False
        student2.course = course1
        student2.year = 1
        student2.save()
        student3 = stuff[3]
        student3.active = True
        student3.course = course2
        student3.year = 1
        student3.save()
        student4 = stuff[4]
        student4.active = True
        student4.course = course3
        student4.year = 1
        student4.save()
        student5 = stuff[5]
        student5.active = True
        student5.course = course3
        student5.year = 2
        student5.save()
        url = (
            '/edit_exam_ids/' +
            subject_area1.slug +
            '/1/'
        )
        request = self.factory.get(url)
        request.user = self.user
        response = edit_exam_ids(request, subject_area1.slug, '1')
        self.assertContains(response, student1.student_id)
        self.assertNotContains(response, student2.student_id)
        self.assertNotContains(response, student3.student_id)
        self.assertContains(response, student4.student_id)
        self.assertNotContains(response, student5.student_id)

    def test_existing_exam_ids_are_shown(self):
        subject_area = SubjectArea.objects.create(name="Cartoon Studies")
        course = Course.objects.create(
            title="MA in Cartoon Studies",
            short_title="Cartoon Studies"
        )
        course.subject_areas.add(subject_area)
        stuff = set_up_stuff()
        student1 = stuff[1]
        student1.active = True
        student1.course = course
        student1.year = 1
        student1.exam_id = '1234'
        student1.save()
        student2 = stuff[2]
        student2.active = True
        student2.course = course
        student2.year = 1
        student2.exam_id = '56789ABC'
        student2.save()
        url = (
            '/edit_exam_ids/' +
            subject_area.slug +
            '/1/'
        )
        request = self.factory.get(url)
        request.user = self.user
        response = edit_exam_ids(request, subject_area.slug, '1')
        self.assertContains(response, '1234')
        self.assertContains(response, '56789ABC')

    def test_exam_ids_get_saved_properly(self):
        subject_area = SubjectArea.objects.create(name="Cartoon Studies")
        course = Course.objects.create(
            title="MA in Cartoon Studies",
            short_title="Cartoon Studies"
        )
        course.subject_areas.add(subject_area)
        stuff = set_up_stuff()
        student1 = stuff[1]
        student1.active = True
        student1.course = course
        student1.year = 1
        student1.save()
        student2 = stuff[2]
        student2.active = True
        student2.course = course
        student2.year = 1
        student2.save()
        student3 = stuff[3]
        student3.active = True
        student3.course = course
        student3.year = 1
        student3.save()
        url = (
            '/edit_exam_ids/' +
            subject_area.slug +
            '/1/'
        )
        request = self.factory.post(
            url,
            data={
                student1.student_id: '1234',
                student2.student_id: '56789E',
                student3.student_id: ''
            }
        )
        request.user = self.user
        response = edit_exam_ids(request, subject_area.slug, '1')
        student1_out = Student.objects.get(student_id=student1.student_id)
        student2_out = Student.objects.get(student_id=student2.student_id)
        student3_out = Student.objects.get(student_id=student3.student_id)
        self.assertEqual(student1_out.exam_id, '1234')
        self.assertEqual(student2_out.exam_id, '56789E')
        self.assertEqual(student3_out.exam_id, None)


class ConcessionsTest(AdminUnitTest):
    """Testing the concessions form"""

    def test_concessions_form_uses_right_template(self):
        module = create_module()
        response = self.client.get(module.get_concessions_url('first'))
        self.assertTemplateUsed(response, 'concessions.html')

    def test_all_active_students_appear_in_template(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student1 = stuff[1]
        student2 = stuff[2]
        student3 = stuff[3]
        student3.active = False
        student3.save()
        request = self.factory.get(module.get_concessions_url('first'))
        request.user = self.user
        response = concessions(request, module.code, module.year, 'first')
        self.assertContains(response, student1.short_name())
        self.assertContains(response, student2.short_name())
        self.assertNotContains(response, student3.short_name())

    def test_correct_names_for_values_in_template(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student1 = stuff[1]
        student2 = stuff[2]
        assessment1 = Assessment.objects.create(
            module=module,
            title="Assessment 1"
        )
        assessment2 = Assessment.objects.create(
            module=module,
            title="Assessment 2"
        )
        performance1 = Performance.objects.get(module=module, student=student1)
        assessment_result_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=38,
            concessions='N'
        )
        assessment_result_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=38,
            concessions='G'
        )
        performance1.assessment_results.add(assessment_result_1)
        performance1.assessment_results.add(assessment_result_2)
        request = self.factory.get(module.get_concessions_url('first'))
        request.user = self.user
        response = concessions(request, module.code, module.year, 'first')
        tag_name_1_1 = (
            'name="' +
            student1.student_id +
            '_' +
            assessment1.slug +
            '"'
        )
        tag_name_1_2 = (
            'name="' +
            student1.student_id +
            '_' +
            assessment2.slug +
            '"'
        )
        self.assertContains(response, tag_name_1_1)
        self.assertContains(response, tag_name_1_2)
        tag_name_2_1 = (
            'name="' +
            student2.student_id +
            '_' +
            assessment1.slug +
            '"'
        )
        tag_name_2_2 = (
            'name="' +
            student2.student_id +
            '_' +
            assessment2.slug +
            '"'
        )
        self.assertContains(response, tag_name_2_1)
        self.assertContains(response, tag_name_2_2)

    def test_existing_concessions_are_displayed(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student1 = stuff[1]
        assessment1 = Assessment.objects.create(
            module=module,
            title="Assessment 1"
        )
        assessment2 = Assessment.objects.create(
            module=module,
            title="Assessment 2"
        )
        performance1 = Performance.objects.get(module=module, student=student1)
        assessment_result_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=38,
            concessions='N'
        )
        assessment_result_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=38,
            concessions='G'
        )
        performance1.assessment_results.add(assessment_result_1)
        performance1.assessment_results.add(assessment_result_2)
        request = self.factory.get(module.get_concessions_url('first'))
        request.user = self.user
        response = concessions(request, module.code, module.year, 'first')
        soup = BeautifulSoup(response.content)
        tag_name_1_1 = (
            '#' +
            student1.student_id +
            '_' +
            assessment1.slug
        )
        select1 = str(soup.select(tag_name_1_1)[0])
        options1 = select1.split('<option')
        for part in options1:
            if 'value="N"' in part:
                option1 = part
        self.assertIn('selected', option1)
        tag_name_1_2 = (
            '#' +
            student1.student_id +
            '_' +
            assessment2.slug
        )
        select2 = str(soup.select(tag_name_1_2)[0])
        options2 = select2.split('<option')
        for part in options2:
            if 'value="N"' in part:
                option2 = part
        self.assertNotIn('selected', option2)
        for part in options2:
            if 'value="G"' in part:
                option2 = part
        self.assertIn('selected', option2)

    def test_submitting_the_form_saves_concessions(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student1 = stuff[1]
        student2 = stuff[2]
        assessment1 = Assessment.objects.create(
            module=module,
            title="Assessment 1"
        )
        assessment2 = Assessment.objects.create(
            module=module,
            title="Assessment 2"
        )
        performance1 = Performance.objects.get(module=module, student=student1)
        assessment_result_1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=38,
            concessions='N'
        )
        assessment_result_2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=38,
            concessions='G'
        )
        performance1.assessment_results.add(assessment_result_1)
        performance1.assessment_results.add(assessment_result_2)
        tag_name_1_1 = (
            student1.student_id +
            '_' +
            assessment1.slug
        )
        tag_name_1_2 = (
            student1.student_id +
            '_' +
            assessment2.slug
        )
        tag_name_2_1 = (
            student2.student_id +
            '_' +
            assessment1.slug
        )
        tag_name_2_2 = (
            student2.student_id +
            '_' +
            assessment2.slug
        )
        request = self.factory.post(
            module.get_concessions_url('first'),
            data={
                tag_name_1_1: 'G',
                tag_name_1_2: 'P',
                tag_name_2_1: 'N',
                tag_name_2_2: 'G',
            }
        )
        request.user = self.user
        response = concessions(request, module.code, module.year, 'first')
        assessment_result_1_1_out = AssessmentResult.objects.get(
            assessment = assessment1,
            part_of = performance1
        )
        assessment_result_1_2_out = AssessmentResult.objects.get(
            assessment = assessment2,
            part_of = performance1
        )
        performance2 = Performance.objects.get(module=module, student=student2)
        assessment_result_2_1_out = AssessmentResult.objects.get(
            assessment = assessment1,
            part_of = performance2
        )
        assessment_result_2_2_out = AssessmentResult.objects.get(
            assessment = assessment2,
            part_of = performance2
        )
        self.assertEqual(assessment_result_1_1_out.concessions, 'G')
        self.assertEqual(assessment_result_1_2_out.concessions, 'P')
        self.assertEqual(assessment_result_2_1_out.concessions, 'N')
        self.assertEqual(assessment_result_2_2_out.concessions, 'G')


class NextYearTest(MainAdminUnitTest):
    """Testing the switch to the next year with all its complications"""

    def populate_db_with_students(self):
        subject_area_1 = SubjectArea.objects.create(name="Cartoon Studies")
        subject_area_2 = SubjectArea.objects.create(name="Evil Plotting")
        course_1 = Course.objects.create(
            title='BA in Cartoon Studies',
            short_title='Cartoon Studies',
        )
        course_1.subject_areas.add(subject_area_1)
        course_2 = Course.objects.create(
            title='BA in Evil Plotting',
            short_title='Evil Plotting',
        )
        course_2.subject_areas.add(subject_area_2)
        course_3 = Course.objects.create(
            title='BA in Cartoon Studies with Evil Plotting',
            short_title='Cartoon Studies / Evil Plotting',
        )
        course_3.subject_areas.add(subject_area_1)
        course_3.subject_areas.add(subject_area_2)
        students = {}
        student1_1 = Student.objects.create(
            first_name='Bugs',
            last_name='Bunny',
            student_id='bb23',
            year=1,
            course=course_1,
        )
        students['1-2'] = student1_1
        student1_2 = Student.objects.create(
            first_name='Daffy',
            last_name='Duck',
            student_id='dd42',
            year=1,
            is_part_time=True,
            course=course_1
        )
        students['1-spty'] = student1_2
        student1_3 = Student.objects.create(
            first_name='Silvester',
            last_name='Cat',
            student_id='sc23',
            year=1,
            is_part_time=True,
            second_part_time_year=True,
            course=course_1
        )
        students['spty-2'] = student1_3
        student1_4 = Student.objects.create(
            first_name='While E',
            last_name='Coyote',
            student_id='wec23',
            year=1,
            course=course_3
        )
        students['mixed_course'] = student1_4
        student2_1 = Student.objects.create(
            first_name='Tweety',
            last_name='Bird',
            student_id='tb23',
            year=2,
            course=course_1
        )
        students['2-3'] = student2_1
        student3_1 = Student.objects.create(
            first_name='Tasmanian',
            last_name='Devil',
            student_id='td23',
            year=3,
            course=course_1
        )
        students['3-4'] = student3_1
        student4_1 = Student.objects.create(
            first_name='Marvin',
            last_name='Martian',
            student_id='mm23',
            year=1,
            course=course_2
        )
        students['different_course'] = student4_1
        return students

    def test_enter_student_progression_uses_correct_template(self):
        students = self.populate_db_with_students()
        response = self.client.get(
            '/enter_student_progression/cartoon-studies/1/'
        )
        self.assertTemplateUsed(response, 'enter_student_progression.html')

    def test_enter_student_progression_shows_correct_students(self):
        students = self.populate_db_with_students()
        request = self.factory.get(
            '/enter_student_progression/cartoon-studies/1/'
        )
        request.user = self.user
        response = enter_student_progression(
            request, 'cartoon-studies', '1')
        self.assertContains(response, students['1-2'].student_id)
        self.assertContains(response, students['1-spty'].student_id)
        self.assertContains(response, students['mixed_course'].student_id)
        self.assertNotContains(
            response, students['different_course'].student_id)
        self.assertNotContains(response, students['2-3'].student_id)
        self.assertNotContains(response, students['3-4'].student_id)

    def test_pass_and_proceed(self):
        student = Student.objects.create(
            first_name="Bugs",
            last_name="Bunny",
            student_id="bb23",
            year=1,
            next_year='PP'
        )
        this_year = int(Setting.objects.get(name="current_year").value)
        next_year = str(this_year + 1)
        request = self.factory.get(reverse('proceed_to_next_year'))
        request.user = self.user
        response = proceed_to_next_year(request)
        student_out = Student.objects.first()
        self.assertEqual(student_out.year, 2)
        new_year = Setting.objects.get(name="current_year").value
        self.assertEqual(new_year, next_year)

    def test_pass_and_proceed_for_part_time_student(self):
        student1 = Student.objects.create(
            first_name="Bugs",
            last_name="Bunny",
            student_id="bb23",
            year=1,
            is_part_time=True,
            next_year='PP'
        )
        student2 = Student.objects.create(
            first_name="Daffy",
            last_name="Duck",
            student_id="dd23",
            year=1,
            is_part_time=True,
            second_part_time_year=True,
            next_year='PP'
        )
        request = self.factory.get(reverse('proceed_to_next_year'))
        request.user = self.user
        response = proceed_to_next_year(request)
        student1_out = Student.objects.get(first_name="Bugs")
        student2_out = Student.objects.get(first_name="Daffy")
        self.assertEqual(student1_out.year, 1)
        self.assertTrue(student1_out.second_part_time_year)
        self.assertEqual(student2_out.year, 2)
        self.assertFalse(student2_out.second_part_time_year)

    def test_pass_and_proceed_with_qld_resit(self):
        student = Student.objects.create(
            first_name="Bugs",
            last_name="Bunny",
            student_id="bb23",
            year=1,
            qld=True,
            next_year='PQ'
        )
        this_year = int(Setting.objects.get(name="current_year").value)
        module = Module.objects.create(
            title="Carrot Eating",
            code="CE23",
            year=this_year,
            foundational=True
        )
        assessment1 = Assessment.objects.create(
            title="Essay",
            value=20
        )
        assessment2 = Assessment.objects.create(
            title="Exam",
            value=80
        )
        result1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=38,
            resit_mark=38
        )
        result2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=80,
        )
        performance = Performance.objects.create(
            student=student,
            module=module,
            belongs_to_year=1
        )
        performance.assessment_results.add(result1)
        performance.assessment_results.add(result2)
        self.assertEqual(performance.qld_failures_after_resit(), [result1])
        request = self.factory.get(reverse('proceed_to_next_year'))
        request.user = self.user
        response = proceed_to_next_year(request)
        student_out = Student.objects.first()
        self.assertEqual(student_out.year, 2)
        comment_str = (
            'In Year 2, Bugs will have to resit Carrot Eating ' +
            '(Essay) for QLD purposes'
        )
        self.assertEqual(student_out.notes, comment_str)

    def test_pass_and_proceed_with_trailed_resits(self):
        student = Student.objects.create(
            first_name="Bugs",
            last_name="Bunny",
            student_id="bb23",
            year=1,
            qld=True,
            next_year='PT'
        )
        this_year = int(Setting.objects.get(name="current_year").value)
        module = Module.objects.create(
            title="Carrot Eating",
            code="CE23",
            year=this_year,
            foundational=True
        )
        assessment1 = Assessment.objects.create(
            title="Essay",
            value=20
        )
        assessment2 = Assessment.objects.create(
            title="Exam",
            value=80
        )
        result1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=38,
        )
        result2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=35,
        )
        performance = Performance.objects.create(
            student=student,
            module=module,
            belongs_to_year=1
        )
        performance.assessment_results.add(result1)
        performance.assessment_results.add(result2)
        performance.calculate_average()
        request = self.factory.get(reverse('proceed_to_next_year'))
        request.user = self.user
        response = proceed_to_next_year(request)
        student_out = Student.objects.first()
        self.assertEqual(student_out.year, 2)
        comment_str = (
            'In Year 2, Bugs will have to resit Carrot Eating ' +
            '(Essay); Carrot Eating (Exam) (trailed)'
        )
        self.assertEqual(student_out.notes, comment_str)

    def test_pass_and_proceed_with_compensation(self):
        student = Student.objects.create(
            first_name="Bugs",
            last_name="Bunny",
            student_id="bb23",
            year=1,
            qld=True,
            next_year='PC'
        )
        this_year = int(Setting.objects.get(name="current_year").value)
        module = Module.objects.create(
            title="Carrot Eating",
            code="CE23",
            year=this_year,
            foundational=True
        )
        assessment1 = Assessment.objects.create(
            title="Essay",
            value=20
        )
        assessment2 = Assessment.objects.create(
            title="Exam",
            value=80
        )
        result1 = AssessmentResult.objects.create(
            assessment=assessment1,
            mark=38,
        )
        result2 = AssessmentResult.objects.create(
            assessment=assessment2,
            mark=35,
        )
        performance = Performance.objects.create(
            student=student,
            module=module,
            belongs_to_year=1
        )
        performance.assessment_results.add(result1)
        performance.assessment_results.add(result2)
        performance.calculate_average()
        request = self.factory.get(reverse('proceed_to_next_year'))
        request.user = self.user
        response = proceed_to_next_year(request)
        student_out = Student.objects.first()
        self.assertEqual(student_out.year, 2)
        comment_str = 'Failure in %s (%s) has been compensated' %(
                module.title, performance.real_average)
        self.assertEqual(student_out.notes, comment_str)

    def test_repeat_year_works(self):
        student = Student.objects.create(
            first_name="Bugs",
            last_name="Bunny",
            student_id="bb23",
            year=1,
            next_year='R'
        )
        this_year = int(Setting.objects.get(name="current_year").value)
        next_year = str(this_year + 1)
        request = self.factory.get(reverse('proceed_to_next_year'))
        request.user = self.user
        response = proceed_to_next_year(request)
        student_out = Student.objects.first()
        self.assertEqual(student_out.year, 1)
        new_year = Setting.objects.get(name="current_year").value
        self.assertEqual(new_year, next_year)
        self.assertEqual(student_out.notes, 'Repeated Year 1')

    def test_repeat_year_absj_works(self):
        student = Student.objects.create(
            first_name="Bugs",
            last_name="Bunny",
            student_id="bb23",
            year=1,
            next_year='ABSJ'
        )
        this_year = int(Setting.objects.get(name="current_year").value)
        next_year = str(this_year + 1)
        request = self.factory.get(reverse('proceed_to_next_year'))
        request.user = self.user
        response = proceed_to_next_year(request)
        student_out = Student.objects.first()
        self.assertEqual(student_out.year, 1)
        new_year = Setting.objects.get(name="current_year").value
        self.assertEqual(new_year, next_year)
        self.assertEqual(student_out.notes, 'Repeated Year 1 ABSJ')

    def test_graduate_with_first(self):
        student = Student.objects.create(
            first_name="Bugs",
            last_name="Bunny",
            student_id="bb23",
            year=3,
            next_year='1'
        )
        request = self.factory.get(reverse('proceed_to_next_year'))
        request.user = self.user
        response = proceed_to_next_year(request)
        student_out = Student.objects.first()
        self.assertEqual(student_out.year, 9)
        self.assertTrue(student_out.active)
        self.assertEqual(student_out.achieved_degree, 1)

    def test_graduate_with_21(self):
        student = Student.objects.create(
            first_name="Bugs",
            last_name="Bunny",
            student_id="bb23",
            year=3,
            next_year='21'
        )
        request = self.factory.get(reverse('proceed_to_next_year'))
        request.user = self.user
        response = proceed_to_next_year(request)
        student_out = Student.objects.first()
        self.assertEqual(student_out.year, 9)
        self.assertTrue(student_out.active)
        self.assertEqual(student_out.achieved_degree, 21)

    def test_graduate_with_22(self):
        student = Student.objects.create(
            first_name="Bugs",
            last_name="Bunny",
            student_id="bb23",
            year=3,
            next_year='22'
        )
        request = self.factory.get(reverse('proceed_to_next_year'))
        request.user = self.user
        response = proceed_to_next_year(request)
        student_out = Student.objects.first()
        self.assertEqual(student_out.year, 9)
        self.assertTrue(student_out.active)
        self.assertEqual(student_out.achieved_degree, 22)

    def test_graduate_with_3rd(self):
        student = Student.objects.create(
            first_name="Bugs",
            last_name="Bunny",
            student_id="bb23",
            year=3,
            next_year='3'
        )
        request = self.factory.get(reverse('proceed_to_next_year'))
        request.user = self.user
        response = proceed_to_next_year(request)
        student_out = Student.objects.first()
        self.assertEqual(student_out.year, 9)
        self.assertTrue(student_out.active)
        self.assertEqual(student_out.achieved_degree, 3)

    def test_graduate_with_cert_he(self):
        student = Student.objects.create(
            first_name="Bugs",
            last_name="Bunny",
            student_id="bb23",
            year=3,
            next_year='C'
        )
        request = self.factory.get(reverse('proceed_to_next_year'))
        request.user = self.user
        response = proceed_to_next_year(request)
        student_out = Student.objects.first()
        self.assertEqual(student_out.year, 9)
        self.assertTrue(student_out.active)
        self.assertEqual(student_out.achieved_degree, 7)

    def test_graduate_with_dipl_he(self):
        student = Student.objects.create(
            first_name="Bugs",
            last_name="Bunny",
            student_id="bb23",
            year=3,
            next_year='D'
        )
        request = self.factory.get(reverse('proceed_to_next_year'))
        request.user = self.user
        response = proceed_to_next_year(request)
        student_out = Student.objects.first()
        self.assertEqual(student_out.year, 9)
        self.assertTrue(student_out.active)
        self.assertEqual(student_out.achieved_degree, 6)

    def test_graduate_with_ordinary_degree(self):
        student = Student.objects.create(
            first_name="Bugs",
            last_name="Bunny",
            student_id="bb23",
            year=3,
            next_year='O'
        )
        request = self.factory.get(reverse('proceed_to_next_year'))
        request.user = self.user
        response = proceed_to_next_year(request)
        student_out = Student.objects.first()
        self.assertEqual(student_out.year, 9)
        self.assertTrue(student_out.active)
        self.assertEqual(student_out.achieved_degree, 5)

    def test_withdraw_student(self):
        student = Student.objects.create(
            first_name="Bugs",
            last_name="Bunny",
            student_id="bb23",
            year=3,
            next_year='WD'
        )
        request = self.factory.get(reverse('proceed_to_next_year'))
        request.user = self.user
        response = proceed_to_next_year(request)
        student_out = Student.objects.first()
        self.assertEqual(student_out.year, 9)
        self.assertTrue(student_out.active)
        self.assertEqual(student_out.achieved_degree, 8)

    def test_proceed_to_next_year_with_multiple_students(self):
        students = self.populate_db_with_students()
        for student in students:
            students[student].next_year = 'PP'
            students[student].save()
        students['3-4'].next_year = '1'
        students['3-4'].save()
        request = self.factory.get(reverse('proceed_to_next_year'))
        request.user = self.user
        response = proceed_to_next_year(request)
        student_1_2 = Student.objects.get(
            student_id=students['1-2'].student_id)
        self.assertEqual(student_1_2.year, 2)
        student_1_spty = Student.objects.get(
            student_id=students['1-spty'].student_id)
        self.assertEqual(student_1_spty.year, 1)
        self.assertTrue(student_1_spty.second_part_time_year)
        student_spty_2 = Student.objects.get(
            student_id=students['spty-2'].student_id)
        self.assertEqual(student_spty_2.year, 2)
        self.assertFalse(student_spty_2.second_part_time_year)
        student_2_3 = Student.objects.get(
            student_id=students['2-3'].student_id)
        self.assertEqual(student_2_3.year, 3)
        student_3_4 = Student.objects.get(
            student_id=students['3-4'].student_id)
        self.assertEqual(student_3_4.year, 9)
        self.assertEqual(student_3_4.achieved_degree, 1)
