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

    def test_teachers_see_students_categories_for_their_areas(self):
        stuff = set_up_stuff()
        subject_area = create_subject_area()
        course = Course.objects.create(title="BA in Cartoon Studies")
        course.subject_areas.add(subject_area)
        self.user.staff.subject_areas.add(subject_area)
        student1 = stuff[1]
        student1.course = course
        student1.year = 1
        student1.save()
        student2 = stuff[2]
        student2.course = course
        student2.year = 2
        student2.save()
        student3 = stuff[3]
        student3.year = 3  # Not in teachers' subject areas
        student3.save()
        student4 = stuff[4]
        student4.course = course
        student4.year = 8
        student4.save()
        student5 = stuff[5]
        student5.year = 9
        student5.course = course
        student5.active = False
        student5.save()
        request = self.factory.get('/')
        request.user = self.user
        response = home(request)
        soup = BeautifulSoup(response.content)
        student_categories = str(soup.select('#menu-student-list'))
        students = Student.objects.all()
        self.assertTrue('Year 1' in student_categories)
        self.assertTrue('<a href="/students/1/">' in student_categories)
        self.assertTrue('Year 2' in student_categories)
        self.assertTrue('<a href="/students/2/">' in student_categories)
        self.assertFalse('Year 3' in student_categories)
        self.assertFalse('<a href="/students/3/">' in student_categories)
        self.assertTrue('PhD' in student_categories)
        self.assertTrue('<a href="/students/8/">' in student_categories)
        self.assertFalse('Alumni' in student_categories)
        self.assertTrue('Inactive Students' in student_categories)
        self.assertTrue('<a href="/students/inactive/">' in student_categories)

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

    def test_main_admin_sees_all_student_categories(self):
        stuff = set_up_stuff()
        subject_area = create_subject_area()
        course = Course.objects.create(title="BA in Cartoon Studies")
        course.subject_areas.add(subject_area)
        self.user.staff.subject_areas.add(subject_area)
        self.user.staff.main_admin = True
        self.user.staff.save()
        student1 = stuff[1]
        student1.course = course
        student1.year = 1
        student1.save()
        student2 = stuff[2]
        student2.course = course
        student2.year = 2
        student2.save()
        student3 = stuff[3]
        student3.course = course
        student3.year = 7
        student3.save()
        student4 = stuff[4]
        student4.course = course
        student4.year = 9
        student4.save()
        student5 = stuff[5]
        student5.year = 1
        student5.active = False
        student5.save()
        request = self.factory.get('/')
        request.user = self.user
        response = home(request)
        soup = BeautifulSoup(response.content)
        student_categories = str(soup.select('#menu-student-list'))
        self.assertTrue('Year 1' in student_categories)
        self.assertTrue('<a href="/students/1/">' in student_categories)
        self.assertTrue('Year 2' in student_categories)
        self.assertTrue('<a href="/students/2/">' in student_categories)
        self.assertFalse('Year 3' in student_categories)
        self.assertFalse('<a href="/students/3/">' in student_categories)
        self.assertTrue('Masters' in student_categories)
        self.assertTrue('<a href="/students/7/">' in student_categories)
        self.assertTrue('Alumni' in student_categories)
        self.assertTrue('<a href="/students/9/">' in student_categories)
        self.assertTrue('Inactive Students' in student_categories)
        self.assertTrue('<a href="/students/inactive/">' in student_categories)
