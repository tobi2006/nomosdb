import sys
from django.test import LiveServerTestCase
from selenium import webdriver
from main.models import Student, Module, Course, SubjectArea


class FunctionalTest(LiveServerTestCase):

    #    @classmethod
#    def setUpClass(cls):
#        for arg in sys.argv:
#            if 'liveserver' in arg:
#                cls.server_url = 'http://' + arg.split('=')[1]
#                return
#        super().setUpClass()
#        cls.server_url = cls.live_server_url
#
#    @classmethod
#    def tearDownClass(cls):
#        if cls.server_url == cls.live_server_url:
#            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_entry_in_table(self, table_id, row_text):
        table = self.browser.find_element_by_id(table_id)
        rows = table.find_elements_by_tag_name('td')
        self.assertIn(row_text, [row.text for row in rows])

    def set_up_test_conditions(self):
        subject1 = SubjectArea.objects.create(name="Witchcraft")
        subject2 = SubjectArea.objects.create(name="Alchemy")
        subject3 = SubjectArea.objects.create(name="Fighting")
        course = Course.objects.create(
            title="BA in Wizard Stuff",
            short_title="WzS"
        )
        course.subject_areas.add(subject1)
        course.subject_areas.add(subject2)
        course.save()
        course2 = Course.objects.create(
            title="BA in Warrior Studies",
            short_title="WarS"
        )
        course2.subject_areas.add(subject3)
        course2.save()
        student1 = Student.objects.create(
            last_name="Baggins",
            first_name="Frodo",
            student_id="FB4223",
            course=course
        )
        student2 = Student.objects.create(
            last_name="Gamgee",
            first_name="Samwise",
            student_id="SG2342",
            course=course2
        )
        module = Module.objects.create(
            title="History of Alchemy",
            code="hoa101",
            year=2014
        )
        module.subject_areas.add(subject2)
        module.save()
