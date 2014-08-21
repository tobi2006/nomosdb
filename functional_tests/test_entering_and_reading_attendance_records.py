from .base import FunctionalTest
from main.models import Module, Student, Performance
from time import sleep

class EnteringAttendanceAndSeeingItInModuleView(FunctionalTest):
    self.set_up_test_conditions(enroll=True)
    module = Module.objects.first()

    # Aragorn wants to record the attendance and goes to his module's
    # page.
    
    self.browser.get(self.live_server_url + module.get_absolute_url())
    self.browser.find_element_by_id('attendance').click()
