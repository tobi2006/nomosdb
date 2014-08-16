from django.test import TestCase
from nomosdb.unisettings import UNI_NAME
from main.models import Student, Module, Course, SubjectArea, Performance


def create_student():
    student = Student.objects.create(
        student_id="fb4223",
        last_name="Baggins",
        first_name="Frodo",
        year="1",
        qld=True
    )
    return student


class HomePageTest(TestCase):

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_title_contains_uni_name(self):
        response = self.client.get('/')
        self.assertContains(response, UNI_NAME)


class StudentViewTest(TestCase):

    def test_student_view_renders_student_view_template(self):
        student = create_student()
        response = self.client.get(student.get_absolute_url())
        self.assertTemplateUsed(response, 'student_view.html')
        self.assertContains(response, "fb4223")
        self.assertContains(response, "Baggins")
        self.assertContains(response, "Frodo")


class AddEditStudentTest(TestCase):

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

    def test_seminar_groups_can_be_saved(self):
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
        Performance.objects.create(student=student1, module=module)
        Performance.objects.create(student=student2, module=module)
        Performance.objects.create(student=student3, module=module)
        response = self.client.post(
            module.get_seminar_groups_url(),
            data={'HW2323': '1', 'SG2342': '2', 'FB4223': '1'}
        )
        performance1 = Performance.objects.get(student=student1, module=module)
        performance2 = Performance.objects.get(student=student2, module=module)
        performance3 = Performance.objects.get(student=student3, module=module)
        self.assertEqual(performance1.seminar_group, 1)
        self.assertEqual(performance2.seminar_group, 2)
        self.assertEqual(performance3.seminar_group, 1)
