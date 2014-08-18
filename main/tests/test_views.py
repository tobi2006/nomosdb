from django.test import TestCase
from nomosdb.unisettings import UNI_NAME
from main.models import Student, Module, Course, SubjectArea, Performance


def create_student():
    """Creates a student to be used by other tests"""
    student = Student.objects.create(
        student_id="fb4223",
        last_name="Baggins",
        first_name="Frodo",
        year="1",
        qld=True
    )
    return student


def set_up_stuff():
    """Sets up a module with five students, enrolls them"""
    module = Module.objects.create(
        title="History of Swordfighting",
        code="HoS101",
        year=2014,
    )
    student1 = Student.objects.create(
        last_name="Baggins",
        first_name="Frodo",
        student_id="FB4223",
    )
    student1.modules.add(module)
    student2 = Student.objects.create(
        last_name="Gamgee",
        first_name="Samwise",
        student_id="SG2342",
    )
    student2.modules.add(module)
    student3 = Student.objects.create(
        last_name="Wurst",
        first_name="Hans",
        student_id="HW2323",
    )
    student3.modules.add(module)
    student4 = Student.objects.create(
        last_name="Schweiss",
        first_name="Axel",
        student_id="AS444"
    )
    student4.modules.add(module)
    student5 = Student.objects.create(
        last_name="Baden",
        first_name="Isolde",
        student_id="IB2323"
    )
    student5.modules.add(module)
    Performance.objects.create(student=student1, module=module)
    Performance.objects.create(student=student2, module=module)
    Performance.objects.create(student=student3, module=module)
    Performance.objects.create(student=student4, module=module)
    Performance.objects.create(student=student5, module=module)
    return((module, student1, student2, student3, student4, student5))


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
        self.assertContains(response, "fb4223")
        self.assertContains(response, "Baggins")
        self.assertContains(response, "Frodo")


class AddEditStudentTest(TestCase):
    """Tests for the student form function"""

    def send_form(self):
        response = self.client.post('/add_student/', data={
            'student_id': 'fb4223',
            'last_name': 'Bäggins',
            'first_name': 'Frodo Middle Names'
        })
        return response

    def test_add_edit_student_renders_right_template(self):
        response = self.client.get('/add_student/')
        self.assertTemplateUsed(response, 'student_form.html')

    def test_add_student_redirects_to_student_view(self):
        response = self.send_form()
        self.assertRedirects(response, '/student/fb4223/')

    def test_add_student_adds_student_to_database(self):
        self.send_form()
        student = Student.objects.first()
        self.assertEqual(student.student_id, 'fb4223')
        self.assertEqual(student.last_name, 'Bäggins')
        self.assertEqual(student.first_name, 'Frodo Middle Names')

    def test_edit_student_shows_correct_data(self):
        student = create_student()
        response = self.client.get(student.get_edit_url())
        self.assertTemplateUsed(response, 'student_form.html')
        self.assertContains(response, 'Baggins')
        self.assertContains(response, 'Frodo')
        self.assertContains(response, 'fb4223')


class ModuleViewTest(TestCase):
    """Tests for the module view"""

    def test_module_view_renders_module_view_template(self):
        module = Module.objects.create(
            title="History of Swordfighting",
            code="HoS101",
            year=2014
        )
        response = self.client.get(module.get_absolute_url())
        self.assertTemplateUsed(response, 'module_view.html')

    def test_performances_in_a_module_are_shown(self):
        module = Module.objects.create(
            title="History of Swordfighting",
            code="HoS101",
            year=2014,
            eligible="1"
        )
        student = Student.objects.create(
            last_name="Wurst",
            first_name="Hans",
            student_id="HW2323",
            year=2
        )
        self.client.post(
            module.get_add_students_url(),
            data={'student_ids': [student.student_id]}
        )
        response = self.client.get(module.get_absolute_url())
        self.assertContains(response, "Wurst, Hans")


class AddStudentsToModuleTest(TestCase):
    """Tests for the function to add students to a module"""

    def test_add_students_to_module_uses_right_template(self):
        module = Module.objects.create(
            title="History of Swordfighting",
            code="HoS101",
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
            title="History of Swordfighting",
            code="HoS101",
            year=2014,
            eligible="1"
        )
        module.subject_areas.add(subject_area1)
        module.save()
        student1 = Student.objects.create(
            last_name="Baggins",
            first_name="Frodo",
            student_id="FB4223",
            course=course,
            year=1
        )
        student2 = Student.objects.create(
            last_name="Gamgee",
            first_name="Samwise",
            student_id="SG2342",
            course=course2,
            year=1
        )
        student3 = Student.objects.create(
            last_name="Wurst",
            first_name="Hans",
            student_id="HW2323",
            course=course,
            year=2
        )
        response = self.client.get(module.get_add_students_url())
        self.assertContains(response, 'Baggins')
        self.assertNotContains(response, 'Gamgee')
        self.assertNotContains(response, 'Wurst')

    def test_submitting_an_empty_form_does_not_break_it(self):
        module = Module.objects.create(
            title="History of Swordfighting",
            code="HoS101",
            year=2014,
            eligible="1"
        )
        response = self.client.post(
            '/add_students_to_module/%s/%s' % (module.code, module.year),
            data={}
        )
        self.assertEqual(response.status_code, 301)

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
                'action': 'Randomly assign',
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
                'action': 'Randomly assign',
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

class AttendanceTest(TestCase):
    """Tests around the attendance function"""

    def test_students_are_shown_according_to_parameter(self):
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
        response = self.client.get(module.get_attendance_url(all))
        self.assertContains(response, student1.last_name)
        self.assertContains(response, student2.last_name)
        self.assertContains(response, student3.last_name)
        self.assertContains(response, student4.last_name)
        self.assertContains(response, student5.last_name)
