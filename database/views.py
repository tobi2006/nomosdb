from django.shortcuts import redirect, render
from nomosdb.unisettings import *
from database.forms import *


def home(request):
    """Simply the home page, nothing there yet"""
    # use if to show different pages for students and teachers!
    return render(request, 'home.html', {})


def add_or_edit_student(request, student_id=None):
    """The form to manually add or edit a student"""
    if student_id:
        student = Student.objects.get(student_id=student_id)
    if request.method == 'POST':
        if student_id:
            form = StudentForm(instance=student, data=request.POST)
        else:
            form = StudentForm(data=request.POST)
        if form.is_valid():
            student = form.save()
            return redirect(student.get_absolute_url())
    else:
        if student_id:
            form = StudentForm(instance=student)
        else:
            form = StudentForm()
    return render(request, 'add_student.html', {'form': form})


def student_view(request, student_id):
    """Shows all information about a student"""
    student = Student.objects.get(student_id=student_id)
    return render(request, 'student_view.html', {'student': student})
