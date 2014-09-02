from .base import *
from bs4 import BeautifulSoup
from main.views import home

class TeacherMenubarTest(TeacherUnitTest):
    """Tests if the right models are contained in the teacher's menubar"""

    def test_teachers_see_only_their_own_modules(self):
        module1 = create_module()
        module2 = Module.objects.create(
            title="Portable Hole Techniques",
            code="pht23",
            year=1900
        )
        self.user.staff.modules.add(module1)
        request = self.factory.get('/')
        request.user = self.user
        response = home(request)
        soup = BeautifulSoup(response.content)
        modules = str(soup.select('#menu-module-list'))
        self.assertTrue(module1.get_absolute_url() in modules)
        self.assertFalse(module2.get_absolute_url() in modules)

    def test_programme_directors_see_all_modules_in_subject_areas(self):
        subject_area1 = SubjectArea.objects.create(name="Cartoon Studies")
        subject_area2 = SubjectArea.objects.create(name="Evil Plotting")
        module1 = create_module()
        module1.subject_areas.add(subject_area1)
        module2 = Module.objects.create(
            title="Portable Hole Techniques",
            code="pht23",
            year=1900
        )
        module2.subject_areas.add(subject_area1)
        module3 = Module.objects.create(
            title="Roadrunner Catching",
            code="rc23",
            year=1900
        )
        module3.subject_areas.add(subject_area2)
        self.user.staff.modules.add(module1)
        self.user.staff.programme_director = True
        self.user.staff.subject_areas.add(subject_area1)
        self.user.staff.save()
        request = self.factory.get('/')
        request.user = self.user
        response = home(request)
        soup = BeautifulSoup(response.content)
        modules = str(soup.select('#menu-module-list'))
        self.assertTrue(module1.get_absolute_url() in modules)
        self.assertTrue(module2.get_absolute_url() in modules)
        self.assertFalse(module3.get_absolute_url() in modules)

class AdminMenubarTest(AdminUnitTest):
    """Tests if the right models are contained in the teacher's menubar"""

    def test_admins_see_all_modules_in_subject_areas(self):
        subject_area1 = SubjectArea.objects.create(name="Cartoon Studies")
        subject_area2 = SubjectArea.objects.create(name="Evil Plotting")
        module1 = create_module()
        module1.subject_areas.add(subject_area1)
        module2 = Module.objects.create(
            title="Portable Hole Techniques",
            code="pht23",
            year=1900
        )
        module2.subject_areas.add(subject_area1)
        module3 = Module.objects.create(
            title="Roadrunner Catching",
            code="rc23",
            year=1900
        )
        module3.subject_areas.add(subject_area2)
        self.user.staff.subject_areas.add(subject_area1)
        request = self.factory.get('/')
        request.user = self.user
        response = home(request)
        soup = BeautifulSoup(response.content)
        modules = str(soup.select('#menu-module-list'))
        self.assertTrue(module1.get_absolute_url() in modules)
        self.assertTrue(module2.get_absolute_url() in modules)
        self.assertFalse(module3.get_absolute_url() in modules)

    def test_main_admin_sees_all_modules(self):
        subject_area1 = SubjectArea.objects.create(name="Cartoon Studies")
        subject_area2 = SubjectArea.objects.create(name="Evil Plotting")
        module1 = create_module()
        module1.subject_areas.add(subject_area1)
        module2 = Module.objects.create(
            title="Portable Hole Techniques",
            code="pht23",
            year=1900
        )
        module2.subject_areas.add(subject_area1)
        module3 = Module.objects.create(
            title="Roadrunner Catching",
            code="rc23",
            year=1900
        )
        module3.subject_areas.add(subject_area2)
        self.user.staff.main_admin = True
        self.user.staff.subject_areas.add(subject_area1)
        self.user.staff.save()
        request = self.factory.get('/')
        request.user = self.user
        response = home(request)
        soup = BeautifulSoup(response.content)
        modules = str(soup.select('#menu-module-list'))
        self.assertTrue(module1.get_absolute_url() in modules)
        self.assertTrue(module2.get_absolute_url() in modules)
        self.assertTrue(module3.get_absolute_url() in modules)
