import sys
from django.test import LiveServerTestCase
from selenium import webdriver


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
