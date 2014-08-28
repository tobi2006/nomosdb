from django.test import TestCase
from nomosdb.unisettings import UNI_NAME
from main.models import *
from bs4 import BeautifulSoup
from .base import *


class HomePageTest(TestCase):
    """Simple tests for the home page"""

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_title_contains_uni_name(self):
        response = self.client.get('/')
        self.assertContains(response, UNI_NAME)


class StudentViewTest(TestCase):
    """Tests for the student view function"""

    def test_student_view_renders_student_view_template(self):
        student = create_student()
        response = self.client.get(student.get_absolute_url())
        self.assertTemplateUsed(response, 'student_view.html')
        self.assertContains(response, "bb23")
        self.assertContains(response, "Bunny")
        self.assertContains(response, "Bugs")


class AddEditStudentTest(TestCase):
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

    def test_add_student_redirects_to_student_view(self):
        response = self.send_form()
        self.assertRedirects(response, '/student/bb23/')

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


class ModuleViewTest(TestCase):
    """Tests for the module view"""

    def test_module_view_renders_module_view_template(self):
        module = Module.objects.create(
            title="Hunting Practice",
            code="hp23",
            year=2014
        )
        response = self.client.get(module.get_absolute_url())
        self.assertTemplateUsed(response, 'module_view.html')

    def test_performances_in_a_module_are_shown(self):
        module = Module.objects.create(
            title="Hunting Practice",
            code="hp23",
            year=2014,
            eligible="1"
        )
        student = Student.objects.create(
            last_name="Pig",
            first_name="Porky",
            student_id="pp2323",
            year=2
        )
        self.client.post(
            module.get_add_students_url(),
            data={'student_ids': [student.student_id]}
        )
        response = self.client.get(module.get_absolute_url())
        self.assertContains(response, "Pig, Porky")


class AddStudentsToModuleTest(TestCase):
    """Tests for the function to add students to a module"""

    def test_add_students_to_module_uses_right_template(self):
        module = Module.objects.create(
            title="Hunting Practice",
            code="hp23",
            year=2014,
            eligible="1"
        )
        response = self.client.get(module.get_add_students_url())
        self.assertTemplateUsed(response, 'add_students_to_module.html')

    def test_only_students_from_same_subject_areas_and_year_are_shown(self):
        subject_area1 = SubjectArea.objects.create(name="Warrior Studies")
        subject_area2 = SubjectArea.objects.create(name="Alchemy")
        course = Course.objects.create(title="BA in Warrior Studies")
        course.subject_areas.add(subject_area1)
        course.save()
        course2 = Course.objects.create(title="BA in Wizard Stuff")
        course2.subject_areas.add(subject_area2)
        course2.save()
        module = Module.objects.create(
            title="Hunting Practice",
            code="hp23",
            year=2014,
            eligible="1"
        )
        module.subject_areas.add(subject_area1)
        module.save()
        student1 = Student.objects.create(
            last_name="Bunny",
            first_name="Bugs",
            student_id="bb23",
            course=course,
            year=1
        )
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
        response = self.client.get(module.get_add_students_url())
        self.assertContains(response, 'Bunny')
        self.assertNotContains(response, 'Duck')
        self.assertNotContains(response, 'Pig')

    def test_submitting_an_empty_form_does_not_break_it(self):
        module = Module.objects.create(
            title="Hunting Practice",
            code="hp23",
            year=2014,
            eligible="1"
        )
        response = self.client.post(
            '/add_students_to_module/%s/%s' % (module.code, module.year),
            data={}
        )
        self.assertEqual(response.status_code, 301)


class RemoveStudentFromModuleTest(TestCase):
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
        response = self.client.get(url)
        self.assertEqual(Performance.objects.count(), 0)
        self.assertEqual(student.modules.count(), 0)


class SeminarGroupTest(TestCase):
    """Tests involving the seminar group setup"""

    def test_seminar_groups_can_be_saved(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student1 = stuff[1]
        student2 = stuff[2]
        student3 = stuff[3]
        response = self.client.post(
            module.get_seminar_groups_url(),
            data={
                'action': 'Save students',
                student1.student_id: '1',
                student2.student_id: '2',
                student3.student_id: '1'
            }
        )
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
        response = self.client.post(
            module.get_seminar_groups_url(),
            data={
                'action': 'Go',
                'ignore': True,
                'number_of_groups': '3'
            }
        )
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
        response = self.client.post(
            module.get_seminar_groups_url(),
            data={
                student2.student_id: '2',
                'action': 'Go',
                'number_of_groups': '3'
            }
        )
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
        response = self.client.get(module.get_seminar_group_overview_url())
        soup = BeautifulSoup(response.content)
        group_1 = str(soup.select('#group_1')[0])
        group_2 = str(soup.select('#group_2')[0])
        self.assertIn(student1.short_name(), group_1)
        self.assertIn(student2.short_name(), group_2)
        self.assertIn(student3.short_name(), group_1)
        self.assertIn(student4.short_name(), group_2)
        self.assertIn(student5.short_name(), group_1)


class AssessmentTest(TestCase):
    """Tests involving setting and deleting of assessments"""

    def test_assessments_page_uses_right_template(self):
        module = set_up_stuff()[0]
        response = self.client.get(module.get_assessment_url())
        self.assertTemplateUsed(response, 'assessment.html')

    def test_assessments_can_be_added_to_module(self):
        module = set_up_stuff()[0]
        self.client.post(
            module.get_assessment_url(),
            data={
                'title': 'Hunting Exercise',
                'value': 40,
            }
        )
        assessment = Assessment.objects.first()
        self.assertEqual(assessment.title, 'Hunting Exercise')
        self.assertEqual(assessment.value, 40)

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
            part_of=performance,
            mark=40
        )
        self.assertEqual(Assessment.objects.count(), 1)
        self.assertEqual(AssessmentResult.objects.count(), 1)
        self.client.get(assessment.get_delete_url())
        self.assertEqual(Assessment.objects.count(), 0)
        self.assertEqual(AssessmentResult.objects.count(), 0)


class AttendanceTest(TestCase):
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
        response = self.client.get(module.get_attendance_url(1))
        self.assertContains(response, student1.last_name)
        self.assertContains(response, student2.last_name)
        self.assertContains(response, student3.last_name)
        self.assertNotContains(response, student4.last_name)
        self.assertNotContains(response, student5.last_name)
        response = self.client.get(module.get_attendance_url(2))
        self.assertNotContains(response, student1.last_name)
        self.assertNotContains(response, student2.last_name)
        self.assertNotContains(response, student3.last_name)
        self.assertContains(response, student4.last_name)
        self.assertContains(response, student5.last_name)
        response = self.client.get(module.get_attendance_url('all'))
        self.assertContains(response, student1.last_name)
        self.assertContains(response, student2.last_name)
        self.assertContains(response, student3.last_name)
        self.assertContains(response, student4.last_name)
        self.assertContains(response, student5.last_name)

    def test_attendance_can_be_added_through_form(self):
        stuff = set_up_stuff()
        module = stuff[0]
        response = self.client.post(
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
        response = self.client.post(
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

class AddEditStaffTest(TestCase):
    """Tests for adding and adding a new staff member"""

    def test_staff_can_be_added_new_user_gets_created(self):
        subject_area = SubjectArea.objects.create(name='Cartoon Studies')
        self.client.post('/add_staff/', data={
            'first_name': 'Elmar',
            'last_name': 'Fudd',
            'email': 'elmar.fudd@acme.edu',
            'subject_areas': ['Cartoon Studies'],
            'role': 'teacher'
        })
        user = User.objects.first()
        staff = Staff.objects.first()
        self.assertEqual(user.staff, staff)
        self.assertEqual(user.last_name, 'Fudd')
        self.assertEqual(user.first_name, 'Elmar')
        self.assertEqual(user.email, 'elmar.fudd@acme.edu')
        self.assertIn(subject_area, staff.subject_areas.all())
        self.assertEqual(staff.role, 'teacher')

    def test_form_for_existing_staff_shows_right_details(self):
        user_in = User.objects.create_user(
            'ef10', 'e.fudd@acme.edu', 'rabbitseason')
        user_in.last_name = 'Fudd'
        user_in.first_name = 'Elmar'
        user_in.save()
        subject_area = SubjectArea.objects.create(name='Cartoon Studies')
        staff_in = Staff.objects.create(user=user_in, role='teacher')
        staff_in.subject_areas.add(subject_area)
        staff_in.save()
        response = self.client.get(staff_in.get_edit_url())
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
        self.client.post(staff_in.get_edit_url(), data={
            'first_name': 'Elmar',
            'last_name': 'Fudd',
            'email': 'elmar.fudd@acme.edu',
            'subject_areas': ['Cartoon Studies'],
            'role': 'admin'
        })
        staff_out = Staff.objects.first()
        self.assertEqual(staff_out.user.last_name, 'Fudd')
        self.assertEqual(staff_out.role, 'admin')


class ViewStaffTest(TestCase):
    """Tests for Viewing Staff Members"""
    
