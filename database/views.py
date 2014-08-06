from django.shortcuts import redirect, render
from nomosdb.unisettings import *
from database.forms import *


def home(request):
    # use if to show different pages for students and teachers!
    return render(request, 'home.html', {})

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(data=request.POST)
        if form.is_valid():
            student = form.save()
            return redirect(student.get_absolute_url())
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})
