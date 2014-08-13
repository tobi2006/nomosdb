from .base import FunctionalTest
from selenium.webdriver.support.ui import Select
from time import sleep


class AddAndEditCourseTest(FunctionalTest):

    def test_course_can_be_added_and_deleted(self):
        self.browser.get(self.live_server_url)

        # Admin Gandalf logs into NomosDB and his greeted with his name

#        self.assertIn( #            'Hello %s' % 'Gandalf',
#            self.browser.find_element_by_tag_name('h1')
#        )

        # Gandalf goes to the admin page of NomosDB to add a new course -
        # the recently validated "BA in Wizard Stuff", comprising of the
        # subject areas Alchemy and Witchcraft.
        self.browser.find_element_by_id('menu-admin').click()

        # First, he adds the subject areas
        self.browser.find_element_by_id('subject_areas').click()
        self.browser.find_element_by_id('id_name').send_keys('Alchemy\n')
        self.browser.find_element_by_id('id_name').send_keys('Witchcraft\n')

        # He can see them above the field

        list_of_subjects = self.browser.find_element_by_id('areas').text
        self.assertIn('Alchemy', list_of_subjects)
        self.assertIn('Witchcraft', list_of_subjects)

        # Happy, he goes back to the admin dashboard and to the courses

        self.browser.find_element_by_id('menu-admin').click()
        self.browser.find_element_by_id('edit_courses').click()
        self.browser.find_element_by_id('add_course').click()

        # Here, he enters his new course.

        self.browser.find_element_by_id('id_title').send_keys(
            'BA in Wizard Stuff')
        self.browser.find_element_by_id('id_short_title').send_keys(
            'BA WS')

        # Unfortunately, I couldn't figure out, how to add the subject
        # areas with Selenium, as I am using a JQuery Plugin called "Chosen"
        # Clicking on it, like in reality, submits the form.
        #
        # Therefore, we submit it without subject areas.

        self.browser.find_element_by_id('submit-id-save').click()

        # Now, there is a brand new course, and I will look further into the
        # Course overview page at some point (low priority).
