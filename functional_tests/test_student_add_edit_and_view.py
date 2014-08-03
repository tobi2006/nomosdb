from .base import FunctionalTest
from time import sleep


class AddStudentTest(FunctionalTest):

    #    def test_first_run_works(self):
#        print(self.live_server_url)
#        #self.browser.get(self.live_server_url)
#        self.browser.get('localhost:8000/')
#        summary = self.browser.find_element_by_id('summary')
#        self.assertIn('It worked!', summary.find_element_by_tag_name('h1'))

    def test_students_can_be_added_manually_and_have_their_own_pages(self):
        self.browser.get(self.live_server_url)

        # Admin Gandalf logs into NomosDB and his greeted with his name

#        self.assertIn(
#            'Hello %s' % 'Gandalf',
#            self.browser.find_element_by_tag_name('h1')
#        )

        # Gandalf adds two students to the database manually by using the
        # Add Student form. He does that by clicking on the word "Students"
        # in the Menubar and there on "Add Student(s)"

        self.browser.find_element_by_id('menu-students').click()
        self.browser.find_element_by_id('menu-add-students').click()

        self.assertIn(
            'Add Student',
            self.browser.find_element_by_tag_name('h1')
        )

        # Now, he enters some detail about the first student.

        self.browser.find_element_by_id('id_first_name').sendKeys('Frodo')
        self.browser.find_element_by_id('id_last_name').sendKeys('Baggins')
        self.browser.find_element_by_id('id_student_id').sendKeys('fb101')
        self.browser.find_element_by_id('id_email').sendKeys(
            'f.baggins@myuni.com'
        )
        self.browser.find_element_by_id('save').click()

        # Gandalf then goes to Frodo's page and checks whether all the
        # data is there.

        self.browser.get(self.live_server_url + '/student/fb101')
        self.check_for_entry_in_table('programme-table', 'fb101')
        self.check_for_entry_in_table('programme-table', 'f.baggins@myuni.com')
