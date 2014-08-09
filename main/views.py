from django.shortcuts import redirect, render
from nomosdb.unisettings import *
from main.forms import *


def home(request):
    """Simply the home page, nothing there yet"""
    # use if to show different pages for students and teachers!
    return render(request, 'home.html', {})


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
