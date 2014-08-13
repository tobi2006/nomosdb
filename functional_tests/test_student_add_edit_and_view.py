from .base import FunctionalTest


class AddAndEditStudentTest(FunctionalTest):

    def test_students_can_be_added_manually_and_have_their_own_pages(self):
        self.browser.get(self.live_server_url)

        # Admin Gandalf logs into NomosDB and his greeted with his name

#        self.assertIn( #            'Hello %s' % 'Gandalf',
#            self.browser.find_element_by_tag_name('h1')
#        )

        # Gandalf adds two students to the database manually by using the
        # Add Student form. He does that by clicking on the word "Students"
        # in the Menubar and there on "Add Student(s)"

        self.browser.find_element_by_id('menu-students').click()
        self.browser.find_element_by_id('menu-add-students').click()

        # Now, he enters some detail about the first student.

        self.browser.find_element_by_id('id_first_name').send_keys('Frodo')
        self.browser.find_element_by_id('id_last_name').send_keys('Baggin')
        self.browser.find_element_by_name('student_id').send_keys('fb101')
        self.browser.find_element_by_id('id_email').send_keys(
            'f.baggins@myuni.com'
        )
        self.browser.find_element_by_id('submit-id-save').click()

        # Gandalf is then directed to Frodo's page and checks whether all the
        # data is there.

        self.check_for_entry_in_table('programme-table', 'fb101')
        self.check_for_entry_in_table('programme-table', 'f.baggins@myuni.com')

        # Alas, Gandalf sees that he made a mistake and clicks on the edit
        # button to be taken to an edit form with Frodo's details

        self.browser.find_element_by_id('edit').click()
        
        # Here, he changes the last name, sees it is in Frodo's page
        # and is happy again.

        self.browser.find_element_by_id('id_last_name').clear()
        self.browser.find_element_by_id('id_last_name').send_keys('Baggins\n')
        self.assertIn(
            ' Baggins',
            self.browser.find_element_by_tag_name('h1').text
        )
