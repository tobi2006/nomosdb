from django.shortcuts import render
from nomosdb.unisettings import *


def home(request):
    # use if to show different pages for students and teachers!

    return render(request, 'home.html', {})

def add_student(request):
    return render(request, 'add_student.html', {})
