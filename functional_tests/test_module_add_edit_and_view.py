from .base import FunctionalTest
from selenium.webdriver.support.ui import Select
from time import sleep


class AddAndEditModuleTest(FunctionalTest):

    def test_teacher_can_add_view_and_edit_module(self):
        self.browser.get(self.live_server_url)

        # Teacher Aragorn logs into NomosDB and his greeted with his name

#        self.assertIn( #            'Hello %s' % 'Aragorn',
#            self.browser.find_element_by_tag_name('h1')
#        )

        # Aragorn adds his new module "History of Swordfighting"
        # to the database manually by using the Add Module form. He does
        # that by clicking on the word "Module" # in the Menubar and there
        # on "Add Module"

        self.browser.find_element_by_id('menu-modules').click()
        self.browser.find_element_by_id('menu-add-module').click()

        # He enters the main details about the module and saves it.

        self.browser.find_element_by_name('code').send_keys('HOS101')
        year_selector = Select(self.browser.find_element_by_name('year'))
        year_selector.select_by_visible_text('2013/14')
        self.browser.find_element_by_name('title').send_keys(
            'History of Swordfighting')
        self.browser.find_element_by_link_text('Assessment').click()
        self.browser.find_element_by_name('assessment_1_title').send_keys(
            'Practical Exercise')
        self.browser.find_element_by_name('assessment_1_value').send_keys('40')
        self.browser.find_element_by_id('submit-id-save').click()

        # Now, he is redirected to the module page and sees it in its
        # full glory.

        headline = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('History of Swordfighting', headline)
        
        # He remembers there, however, that some folks got killed last year
        # and wants to change the nature of the assessment by clicking on the
        # Edit button

        self.browser.find_element_by_id('edit').click()

        self.browser.find_element_by_link_text('Assessment').click()
        self.browser.find_element_by_name('assessment_1_title').clear()
        self.browser.find_element_by_name('assessment_1_title').send_keys(
            'Essay on theory\n')
        all_ths = self.browser.find_elements_by_tag_name('th')
        content = []
        for th in all_ths:
            content.append(th.text)
        self.assertIn(
            'Essay on theory (40 %)',
            content
        )
