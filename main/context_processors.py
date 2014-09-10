from main.unisettings import *
from main.models import *
from main.views import is_teacher, is_admin, is_staff


def constants(request):
    """A few small variables that are used on most pages"""
    return {
        'UNI_NAME': Settings.objects.get(name='uni_name').value,
        'UNI_SHORT_NAME': Settings.objects.get(name='uni_short_name').value,
    }


def menubar(request):
    """Returns the module dictionary for the menubar"""
    if is_staff(request.user):
        staff = request.user.staff
        future = []
        current = []
        past = []
        try:
            current_year = int(Settings.objects.get(name="current_year").value)
        except Settings.DoesNotExist:
            current_year = int(START_YEAR)
            Settings.objects.create(name="current_year", value=current_year)
        staff_subject_areas = staff.subject_areas.all().values('name')
        if staff.role == 'teacher':
            if staff.programme_director:
                modules = Module.objects.filter(
                    subject_areas__name__in=staff_subject_areas)
            else:
                modules = staff.modules.all()
        else:
            if staff.main_admin:
                modules = Module.objects.all()
            else:
                modules = Module.objects.filter(
                    subject_areas__name__in=staff_subject_areas)
        for module in modules:
            if module.year == current_year:
                current.append(module)
            elif module.year > current_year:
                future.append(module)
            elif module.year < current_year:
                past.append(module)
        current.sort(key=lambda x: x.title)
        past.sort(key=lambda x: x.title)
        future.sort(key=lambda x: x.title)
        module_dict = {}
        module_dict['current'] = current
        module_dict['past'] = past
        module_dict['future'] = future

        student_list = []
        other_categories = []
        if staff.main_admin:
            relevant_students = Student.objects.all()
        else:
            relevant_students = Student.objects.filter(
                course__subject_areas__name__in=staff_subject_areas)
        if relevant_students.filter(year=1, active=True).exists():
            student_list.append(('1', 'Year 1'))
        if relevant_students.filter(year=2, active=True).exists():
            student_list.append(('2', 'Year 2'))
        if relevant_students.filter(year=3, active=True).exists():
            student_list.append(('3', 'Year 3'))
        if relevant_students.filter(year=7, active=True).exists():
            student_list.append(('7', 'Masters Students'))
        if relevant_students.filter(year=8, active=True).exists():
            student_list.append(('8', 'PhD Students'))
        if relevant_students.filter(year=9, active=True).exists():
            student_list.append(('9', 'Alumni'))
        if relevant_students.filter(year=None, active=True).exists():
            other_categories.append(
                ('unassigned', 'Students not assigned to a Year')
            )
        if relevant_students.filter(active=False).exists():
            other_categories.append(('inactive', 'Inactive Students'))

    else:
        student_list = []
        module_dict = {}
        other_categories = []
    return {
        'module_dict': module_dict,
        'menu_student_categories': student_list,
        'menu_other_categories': other_categories
    }
