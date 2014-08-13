from django.shortcuts import redirect, render
from nomosdb.unisettings import *
from main.forms import *


def home(request):
    """Simply the home page, nothing there yet"""
    # use if to show different pages for students and teachers!
    return render(request, 'home.html', {})


def admin(request):
    """Opens the admin dashboard"""
    return render(request, 'admin.html', {})


def subject_areas(request):
    subject_areas = SubjectArea.objects.all()
    if request.method == 'POST':
        form = SubjectAreaForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/subject_areas/')
    form = SubjectAreaForm()
    return render(
        request,
        'subject_areas.html',
        {'subject_areas': subject_areas, 'form': form}
    )

def course_overview(request):
    """Page that shows all courses"""
    courses = Course.objects.all()
    return render(request, 'course_overview.html', {'courses': courses})


def add_or_edit_course(request, course_id=None):
    """The form to manually add or edit a course"""
    if course_id:
        edit = True
        course = Course.objects.get(id=course_id)
    else:
        edit = False
    if request.method == 'POST':
        if edit:
            form = CourseForm(instance=course, data=request.POST)
        else:
            form = CourseForm(data=request.POST)
        if form.is_valid():
            course = form.save()
            return redirect(course.get_absolute_url())
    else:
        if edit:
            form = CourseForm(instance=course)
        else:
            form = CourseForm()
    return render(request, 'course_form.html', {'form': form, 'edit': edit})


def add_or_edit_student(request, student_id=None):
    """The form to manually add or edit a student"""
    if student_id:
        edit = True
        student = Student.objects.get(student_id=student_id)
    else:
        edit = False
    if request.method == 'POST':
        if edit:
            form = StudentForm(instance=student, data=request.POST)
        else:
            form = StudentForm(data=request.POST)
        if form.is_valid():
            student = form.save()
            return redirect(student.get_absolute_url())
    else:
        if edit:
            form = StudentForm(instance=student)
        else:
            form = StudentForm()
    return render(request, 'student_form.html', {'form': form, 'edit': edit})


def student_view(request, student_id):
    """Shows all information about a student"""
    student = Student.objects.get(student_id=student_id)
    return render(request, 'student_view.html', {'student': student})


def add_or_edit_module(request, code=None, year=None):
    """The form to add or edit a module"""
    if code and year:
        module = Module.objects.get(code=code, year=year)
        edit = True
    else:
        edit = False
    if request.method == 'POST':
        if edit:
            form = ModuleForm(instance=module, data=request.POST)
        else:
            form = ModuleForm(data=request.POST)
        if form.is_valid():
            module = form.save()
            return redirect(module.get_absolute_url())
    else:
        if edit:
            form = ModuleForm(instance=module)
        else:
            form = ModuleForm()
    return render(request, 'module_form.html', {'form': form, 'edit': edit})


def module_view(request, code, year):
    """Shows all information about a module"""
    module = Module.objects.get(code=code, year=year)
    return render(request, 'module_view.html', {'module': module})


def add_students_to_module(request, code, year):
    """Simple form to add students to a module and create Performance items"""
    module = Module.objects.get(code=code, year=year)
    students_in_module = module.student_set.all()
    if len(module.eligible) > 1:
        more_than_one_year = True
    else:
        more_than_one_year = False
    students = []
    years = []
    for number in module.eligible:
        year = int(number)
        students_this_year = Student.objects.filter(

    return render(request, 'add_students_to_module.html', {})


#
#    for number in module.eligible:
#        year = int(number)  # Find out which students are eligible
#        meta_stuff = MetaData.objects.get(data_id=1)
#        current_year = meta_stuff.current_year
#        time_difference = module.year - current_year
#        year = year - time_difference
#        years.append(year)
#    for student in students_from_db:
#        if student not in students_in_module:
#            students.append(student)
#        if student.year in years:
#            eligible.append(student.student_id)
#
#    if request.method == 'POST':
#        students_to_add = request.POST.getlist('selected_student_id')
#        for student_id in students_to_add:
#            student_to_add = Student.objects.get(student_id=student_id)
#            student_to_add.modules.add(module)
#            # Generate Performance entry for the student
#            performance = Performance(
#                student=student_to_add,
#                module=module
#                )
#            performance.initial_save()
#
#        return HttpResponseRedirect(module.get_absolute_url())
#    return render_to_response(
#        'add_students_to_module.html',
#        {
#            'module': module,
#            'more_than_one_year': more_than_one_year,
#            'students': students,
#            'llb': llb,
#            'eligible': eligible
#        },
#        context_instance=RequestContext(request)
#        )
