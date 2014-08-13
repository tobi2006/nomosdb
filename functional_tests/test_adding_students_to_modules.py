from .base import FunctionalTest
from time import sleep

class AddStudentsToModules(FunctionalTest):

    def test_students_can_be_added_to_database(self):
        self.set_up_test_conditions()
        self.browser.get(self.live_server_url + '/module/hoa101/2014')
        self.browser.find_element_by_id('add_students_to_module').click()
