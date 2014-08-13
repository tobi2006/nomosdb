from django.test import TestCase
from nomosdb.unisettings import UNI_NAME
from main.models import Student, Module, Course, SubjectArea

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

            #class AddEditModuleTest(TestCase):
            #    def test_add_edit_module_renders_right_template(self):
            #        response = self.client.get('/add_module/')
            #        self.assertTemplateUsed(response, 'module_form.html')

class ModuleViewTest(TestCase):

    def test_module_view_renders_module_view_template(self):
        module = Module.objects.create(
            title="History of Swordfighting",
            code="HoS101",
            year=2014
        )
        response = self.client.get(module.get_absolute_url())
        self.assertTemplateUsed(response, 'module_view.html')


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


    def test_only_students_from_the_same_subject_areas_are_shown(self):
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
        response = self.client.get(module.get_add_students_url())
        self.assertContains(response, 'Baggins')
        self.assertNotContains(response, 'Gamgee')
