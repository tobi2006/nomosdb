from django.test import TestCase
from nomosdb.unisettings import UNI_NAME
from database.models import Student

class HomePageTest(TestCase):

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_title_contains_uni_name(self):
        response = self.client.get('/')
        self.assertContains(response, UNI_NAME)

class StudentViewTest(TestCase):

    def test_student_view_renders_student_view_template(self):
        student = Student.objects.create(
            student_id="fb4223",
            last_name="Baggins",
            first_name="Frodo",
            year="1",
            qld=True
        )
        response = self.client.get(student.get_absolute_url())
        self.assertContains(response, "fb4223")
        self.assertContains(response, "Baggins")
        self.assertContains(response, "Frodo")
