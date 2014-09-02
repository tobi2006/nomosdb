from nomosdb.unisettings import *
from main.models import *
from main.views import is_teacher, is_admin, is_staff


def constants(request):
    """A few small variables that are used on most pages"""
    return {
        'UNI_NAME': UNI_NAME,
        'UNI_SHORT_NAME': UNI_SHORT_NAME,
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
        if staff.role == 'teacher':
            if staff.programme_director:
                teacher_subject_areas = staff.subject_areas.all().values(
                    'name')
                modules = Module.objects.filter(
                    subject_areas__name__in=teacher_subject_areas)
            else:
                modules = staff.modules.all()
        else:
            if staff.main_admin:
                modules = Module.objects.all()
            else:
                admin_subject_areas = staff.subject_areas.all().values(
                    'name')
                modules = Module.objects.filter(
                    subject_areas__name__in=admin_subject_areas)
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
    else:
        module_dict = {}
    return {
        'module_dict': module_dict
    }
