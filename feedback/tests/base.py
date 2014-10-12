from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from main.models import *


def set_initial_values():
    """Sets the current year to 1900"""
    Setting.objects.create(name="current_year", value="1900")
    Setting.objects.create(name="uni_name", value="Acme University")
    Setting.objects.create(name="uni_short_name", value="ACME")
    Setting.objects.create(name="nomosdb_url", value="www.warner.com")
    Setting.objects.create(name="admin_email", value="chuck.jones@warner.com")
    Setting.objects.create(name="admin_name", value="Chuck Jones")


def create_student(save=True):
    """Creates a student"""
    student = Student(
        student_id='bb23',
        last_name='Bunny',
        first_name='Bugs Middle Names',
        year=1
    )
    if save:
        student.save()
    return student


def create_module(save=True):
    """Creates a module"""
    module = Module(
        title='Hunting Laws',
        code="hl23",
        year="1900",
    )
    if save:
        module.save()
    return module


def create_user():
    user = User.objects.create_user(
        first_name='Elmar',
        last_name='Fudd',
        username='ef123',
        email='e.fudd@acme.edu',
        password='rabbitseason'
    )
    return user


def create_teacher(save=True):
    user = create_user()
    staff = Staff(user=user, role='teacher')
    if save:
        staff.save()
    return staff


def create_assessment(save=True):
    module = create_module()
    assessment = Assessment(
        module=module,
        title="Essay",
        value=100,
        max_word_count=3000,
        marksheet_type='essay'
    )
    if save:
        assessment.save()
    return assessment


def create_admin(save=True):
    user = User.objects.create_user(
        first_name="Mel",
        last_name="Blank",
        username="mb1000",
        email="mel.blank@acme.edu",
        password="manof1000voices"
    )
    staff = Staff(user=user, role='admin')
    if save:
        staff.save()
    return staff


def set_up_stuff():
    """Sets up a module with five students, enrolls them"""
    module = Module.objects.create(
        title="Hunting Practice",
        code="hp23",
        year=2014,
        first_session=1,
        last_session=12,
        no_teaching_in=7
    )
    student1 = Student.objects.create(
        last_name="Bunny",
        first_name="Bugs",
        student_id="bb23",
        year=1
    )
    student1.modules.add(module)
    student2 = Student.objects.create(
        last_name="Duck",
        first_name="Daffy",
        student_id="dd42",
        year=1
    )
    student2.modules.add(module)
    student3 = Student.objects.create(
        last_name="Pig",
        first_name="Porky",
        student_id="pp2323",
        year=1
    )
    student3.modules.add(module)
    student4 = Student.objects.create(
        last_name="Le Pew",
        first_name="Pepe",
        student_id="plp42",
        year=1
    )
    student4.modules.add(module)
    student5 = Student.objects.create(
        last_name="Devil",
        first_name="Tasmanian",
        student_id="td2323"
    )
    student5.modules.add(module)
    Performance.objects.create(student=student1, module=module)
    Performance.objects.create(student=student2, module=module)
    Performance.objects.create(student=student3, module=module)
    Performance.objects.create(student=student4, module=module)
    Performance.objects.create(student=student5, module=module)
    return((module, student1, student2, student3, student4, student5))


class TeacherUnitTest(TestCase):
    """Sets up the testing environment for a teacher"""

    def setUp(self):
        set_initial_values()
        self.factory = RequestFactory()
        user = User.objects.create_user(
            username="mtm23",
            email="marvin.the.martian@acme.edu",
            password="zapp",
            first_name="Marvin",
            last_name="The Martian"
        )
        teacher = Staff.objects.create(user=user, role='teacher')
        self.user = user


class AdminUnitTest(TestCase):
    """Sets up the testing environment for an admin"""

    def setUp(self):
        set_initial_values()
        self.factory = RequestFactory()
        user = User.objects.create_user(
            username="cj123",
            email="chuck.jones@acme.edu",
            password="cartoongod",
            first_name="Chuck",
            last_name="Jones"
        )
        admin = Staff.objects.create(user=user, role='admin')
        self.user = user
