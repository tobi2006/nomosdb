from .base import FunctionalTest
from time import sleep

class AddStudentsToModules(FunctionalTest):

    def test_students_can_be_added_to_database(self):
        self.set_up_test_conditions()
        # Aragorn wants to populate his module and goes to the page, where
        # he clicks the "Add Students to Module" button
        self.browser.get(self.live_server_url + '/module/hoa101/2014')
        self.browser.find_element_by_id('add_students_to_module').click()
        self.browser.find_element_by_id('cb_FB4223').click()
        self.browser.find_element_by_id('submit').click()
        all_tds = self.browser.find_elements_by_tag_name('td')
        content = []
        for td in all_tds:
            content.append(td.text)
        self.assertIn(
            'Baggins, Frodo',
            content
        )
