from django.test import TestCase
from main.models import *
from main.views import *
from bs4 import BeautifulSoup
from .base import *


class StatusCheckTest(TestCase):
    """Testing the decorator test functions"""

    def test_user_teacher_test_works(self):
        elmar = create_teacher()
        self.assertTrue(is_staff(elmar.user))
        self.assertTrue(is_teacher(elmar.user))
        self.assertFalse(is_admin(elmar.user))

    def test_staff_admin_status_is_properly_undertood_at_login(self):
        admin = create_admin()
        self.assertTrue(is_staff(admin.user))
        self.assertFalse(is_teacher(admin.user))
        self.assertTrue(is_admin(admin.user))


class HomePageTest(TeacherUnitTest):
    """Simple tests for the home page"""

    def test_home_page_renders_home_template(self):
        request = self.factory.get('/')
        request.user = self.user
        response = home(request)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_title_contains_uni_name(self):
        request = self.factory.get('/')
        request.user = self.user
        response = home(request)
        self.assertContains(response, 'Acme University')


class StudentViewTest(TeacherUnitTest):
    """Tests for the student view function"""

    def test_student_view_renders_student_view_template(self):
        student = create_student()
        request = self.factory.get(student.get_absolute_url())
        request.user = self.user
        response = student_view(request, student.student_id)
        self.assertTemplateUsed(response, 'student_view.html')
        self.assertContains(response, "bb23")
        self.assertContains(response, "Bunny")
        self.assertContains(response, "Bugs")


class AddEditStudentTest(TeacherUnitTest):
    """Tests for the student form function"""

    def send_form(self):
        request = self.factory.post(
            '/add_student/',
            data={
                'student_id': 'bb23',
                'last_name': 'Bünny',
                'first_name': 'Bugs Middle Names'
            }
        )
        request.user = self.user
        response = add_or_edit_student(request)
        return response

    def test_add_edit_student_renders_right_template(self):
        request = self.factory.get('/add_student/')
        request.user = self.user
        response = add_or_edit_student(request)
        self.assertTemplateUsed(response, 'student_form.html')

    def test_add_student_adds_student_to_database(self):
        self.send_form()
        student = Student.objects.first()
        self.assertEqual(student.student_id, 'bb23')
        self.assertEqual(student.last_name, 'Bünny')
        self.assertEqual(student.first_name, 'Bugs Middle Names')

    def test_edit_student_shows_correct_data(self):
        student = create_student()
        request = self.factory.get(student.get_edit_url())
        request.user = self.user
        response = add_or_edit_student(request, student.student_id)
        self.assertTemplateUsed(response, 'student_form.html')
        self.assertContains(response, 'Bunny')
        self.assertContains(response, 'Bugs')
        self.assertContains(response, 'bb23')


class ModuleViewTest(TeacherUnitTest):
    """Tests for the module view"""

    def test_module_view_renders_module_view_template(self):
        module = Module.objects.create(
            title="Hunting Practice",
            code="hp23",
            year=1900
        )
        request = self.factory.get(module.get_absolute_url())
        request.user = self.user
        response = module_view(request, module.code, module.year)
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
        request = self.factory.post(
            module.get_add_students_url(),
            data={'student_ids': [student.student_id]}
        )
        request.user = self.user
        response = add_students_to_module(request, module.code, module.year)
        out_request = self.factory.get(module.get_absolute_url())
        out_request.user = self.user
        out_response = module_view(out_request, module.code, module.year)
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
        request = self.factory.get(module.get_absolute_url())
        request.user = self.user
        response = module_view(request, module.code, module.year)
        self.assertContains(response, 'Bunny, Bugs')
        self.assertNotContains(response, 'Pig, Porky')


class AddStudentsToModuleTest(TeacherUnitTest):
    """Tests for the function to add students to a module"""

    def test_add_students_to_module_uses_right_template(self):
        module = create_module()
        request = self.factory.get(module.get_add_students_url())
        request.user = self.user
        response = add_students_to_module(request, module.code, module.year)
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
        request = self.factory.get(module.get_add_students_url())
        request.user = self.user
        response = add_students_to_module(request, module.code, module.year)
        self.assertContains(response, 'Bunny')
        self.assertNotContains(response, 'Duck')
        self.assertNotContains(response, 'Pig')
        self.assertNotContains(response, 'Runner')

    def test_submitting_an_empty_form_does_not_break_it(self):
        module = create_module()
        request = self.factory.post(
            '/add_students_to_module/%s/%s' % (module.code, module.year),
            data={}
        )
        request.user = self.user
        response = add_students_to_module(request, module.code, module.year)
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
        request = self.factory.get(module.get_seminar_group_overview_url())
        request.user = self.user
        response = seminar_group_overview(request, module.code, module.year)
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
        request = self.factory.get(module.get_assessment_url())
        request.user = self.user
        response = assessment(request, module.code, module.year)
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
            part_of=performance,
            mark=40
        )
        self.assertEqual(Assessment.objects.count(), 1)
        self.assertEqual(AssessmentResult.objects.count(), 1)
        request = self.factory.get(assessment.get_delete_url())
        request.user = self.user
        delete_assessment(request, module.code, module.year, assessment.slug)
        self.assertEqual(Assessment.objects.count(), 0)
        self.assertEqual(AssessmentResult.objects.count(), 0)


class AttendanceTest(TeacherUnitTest):
    """Tests around the attendance function"""

    def test_attendance_uses_correct_template(self):
        module = set_up_stuff()[0]
        request = self.factory.get(module.get_attendance_url('all'))
        request.user = self.user
        response = attendance(request, module.code, module.year, 'all')
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
        add_or_edit_staff(request)
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
        add_or_edit_staff(request, user_in.username)
        staff_out = Staff.objects.get(user=user_in)
        self.assertEqual(staff_out.user.last_name, 'Fudd')
        self.assertEqual(staff_out.role, 'admin')


class ViewStaffTest(AdminUnitTest):
    """Tests for Viewing Staff Members"""

    def test_staff_view_by_subject_uses_correct_template(self):
        request = self.factory.get('/view_staff_by_subject/')
        request.user = self.user
        response = view_staff_by_subject(request)
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
        table1 = str(soup.find(id=subject_area_1.slug()))
        self.assertTrue(staff1.name() in table1)
        self.assertTrue(staff2.name() in table1)
        self.assertTrue(staff3.name() in table1)
        table2 = str(soup.find(id=subject_area_2.slug()))
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
        request = self.factory.get('/year_view/all')
        request.user = self.user
        response = year_view(request, 'all')
        self.assertTemplateUsed(response, 'year_view')

    def test_teachers_see_all_students_from_their_subject_areas(self):
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


class CSVParsingTests(AdminUnitTest):
    """Tests for the CSV Parsing"""
    
    def test_csv_data_gets_parsed_properly(self):
        parsed_csvlist = (
            'bb42,Bunny,Bugs,1900,1,bb42@acme.edu,+112345678/////' +
            'dd23,Duck,Daffy,1900,1,dd23@acme.edu,+123456789/////' +
            'pp42,Pig,Porky,1899,2,pp42@acme.edu,+134567890/////' +
            'test,wrong,entry,to,beignored'
        )
        data = Data.objects.create(id='randomstring', value=parsed_csvlist)
        request = self.factory.post('/parse_csv/randomstring/', data={
            'column1': 'student_id',
            'column2': 'last_name',
            'column3': 'first_name',
            'column4': 'since',
            'column5': 'year',
            'column6': 'email',
            'column7': 'phone_no',
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
