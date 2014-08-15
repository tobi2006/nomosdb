from .base import FunctionalTest
from time import sleep

class AddStudentsToModules(FunctionalTest):

    def test_students_can_be_added_to_database(self):
        self.set_up_test_conditions()
        # Aragorn wants to populate his module and goes to the page, where
        # he clicks the "Add Students to Module" button
        self.browser.get(self.live_server_url + '/module/hoa101/2014')
        self.browser.find_element_by_id('add_students_to_module').click()
        #self.browser.find_element_by_name(
