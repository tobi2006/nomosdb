from main.unisettings import *
from main.models import *
from main.views import is_teacher, is_admin, is_staff


def constants(request):
    """A few small variables that are used on most pages"""
    show_admin_menu = False
    if is_staff(request.user):
        if request.user.staff.role == 'admin':
            show_admin_menu = True
        elif request.user.staff.programme_director:
            show_admin_menu = True
    try:
        uni_name = Setting.objects.get(name='uni_name').value
    except Setting.DoesNotExist:
        uni_name = ''
    try:
        uni_short_name = Setting.objects.get(name='uni_short_name').value
        uni_short_name += '@Nomos DB'
    except Setting.DoesNotExist:
        uni_short_name = 'Nomos DB'
    return {
        'UNI_NAME': uni_name,
        'UNI_SHORT_NAME': uni_short_name,
        'show_admin_menu': show_admin_menu,
    }


def menubar(request):
    """Returns the module dictionary for the menubar"""
    if is_staff(request.user):
        staff = request.user.staff
        future = []
        current = []
        past = []
        try:
            current_year = int(Setting.objects.get(name="current_year").value)
        except Setting.DoesNotExist:
            current_year = 2014
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
