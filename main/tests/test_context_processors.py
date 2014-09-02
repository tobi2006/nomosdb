from .base import *
from bs4 import BeautifulSoup

class TeacherMenubarTest(TeacherUnitTest):
    """Tests if the right models are contained in the teacher's menubar"""

    def test_teachers_see_only_their_own_modules(self):
        request = self.factory.get('/')
        request.user = self.user
        response = home(request)
        soup = BeautifulSoup(response.content)
        modules = str(soup.select('#menu-module-list'))
        print(modules)
        
        

    def test_programme_directors_see_all_modules_in_subject_areas(self):
        pass

class AdminMenubarTest(AdminUnitTest):
    """Tests if the right models are contained in the teacher's menubar"""

    def test_admins_see_all_modules_in_subject_areas(self):
        pass

    def test_main_admin_sees_all_modules(self):
        pass
