from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.core.urlresolvers import resolve
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from main.forms import *
from main.functions import week_number, week_starting_date
from main.messages import (
    new_staff_email, attendance_email, password_reset_email
)
from main.models import *
from main.unisettings import *
from random import shuffle, choice
from string import ascii_letters, digits
from reportlab.platypus import (
    Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.flowables import PageBreak


# Authentication

def is_teacher(user):
    if hasattr(user, 'staff'):
        if user.staff.role == 'teacher':
            return True
    return False


def is_admin(user):
    if hasattr(user, 'staff'):
        if user.staff.role == 'admin':
            return True
        elif user.staff.programme_director:
            return True
    return False


def is_pd(user):
    if hasattr(user, 'staff'):
        if user.staff.programme_director:
            return True
        elif user.staff.main_admin:
            return True
    return False


def is_main_admin(user):
    if hasattr(user, 'staff'):
        if user.staff.main_admin is True:
            return True
    return False


def is_staff(user):
    if hasattr(user, 'staff'):
        return True
    else:
        return False


def is_student(user):
    if hasattr(user, 'student'):
        return True
    else:
        return False


def reset_password(request):
    """Sends out a new password by email"""
    if 'email' in request.GET and request.GET['email']:
        email = request.GET['email']
        try:
            user = User.objects.get(email=email)
            username = user.username
            new_password = User.objects.make_random_password()
            user.set_password(new_password)
            user.save()
            if is_staff(user):
                name = user.first_name
            else:
                name = user.student.short_first_name()
            message = password_reset_email(name, username, new_password)
            sender = Setting.objects.get(name='admin_email').value
            send_mail(
                'Your new password on NomosDB',
                message,
                sender,
                [email]
            )
            return redirect('/')
        except User.DoesNotExist:
            return redirect(reverse(wrong_email))
    else:
        return redirect('/')


def wrong_email(request):
    """Small page to show that the password was wrong"""
    example_email = Setting.objects.get(name='example_email').value
    return render(
        request,
        'wrong_password.html',
        {'example_email': example_email}
    )


# Overview pages / general settings


@login_required
def home(request):
    """Home page view for everyone

    This function displays different home pages, depending on whether
    the user is a student or a staff member. If no settings are made yet
    (usually that's the case at the very first login), the user is
    redirected to the settings page.
    """

    if Setting.objects.exists():

        if is_student(request.user):
            # The view for the student, returns a page with marksheets only
            student = Student.objects.get(user=request.user)
            performances = Performance.objects.filter(student=student)
            years = {}
            for performance in performances:
                results = AssessmentResult.objects.filter(part_of=performance)
                this_performance = {
                    'title': performance.module.title,
                    'results': []
                }
                add = False
                for result in results:
                    this_result = {'title': result.assessment.title}
                    url_dict = result.get_marksheet_urls()
                    if result.assessment.available and 'first' in url_dict:
                        this_result['first'] = url_dict['first']
                        add = True
                    if (result.assessment.resit_available and
                            'resit' in url_dict):
                        this_result['resit'] = url_dict['resit']
                        add = True
                    if (result.assessment.second_resit_available and
                            'second_resit' in url_dict):
                        this_result['second_resit'] = url_dict['second_resit']
                        add = True
                    if (result.assessment.qld_resit_available and
                            'qld_resit' in url_dict):
                        this_result['qld_resit'] = url_dict['qld_resit']
                        add = True
                    this_performance['results'].append(this_result)
                year = performance.module.year
                if add:
                    if year in years:
                        years[year].append(this_performance)
                    else:
                        years[year] = [this_performance]
            return render(
                request,
                'student_home.html',
                {'student': student, 'years': years}
            )
        elif is_staff(request.user):
            return render(request, 'home.html', {})
    else:
        return redirect(reverse('main_settings'))


@login_required
@user_passes_test(is_admin)
def admin(request):
    """Opens the admin dashboard"""
    if request.user.staff.main_admin:
        main_admin = True
        staff_subject_areas = SubjectArea.objects.all()
    else:
        main_admin = False
        staff_subject_areas = request.user.staff.subject_areas.all()
    subject_areas = {}
    subject_areas_real_years = {}
    for subject_area in staff_subject_areas:
        if subject_area.courses.exists():
            for course in subject_area.courses.all():
                for year in [1, 2, 3, 7, 8]:
                    if Student.objects.filter(
                            year=year, course=course).exists():
                        if year == 7:
                            year_tpl = (7, 'Masters')
                        elif year == 8:
                            year_tpl = (8, 'PhD')
                        else:
                            year_str = 'Year ' + str(year)
                            year_tpl = (year, year_str)
                        if subject_area in subject_areas:
                            if year_tpl not in subject_areas[subject_area]:
                                subject_areas[subject_area].append(year_tpl)
                        else:
                            subject_areas[subject_area] = [year_tpl]
        real_years = []
        for module in Module.objects.all():
            if subject_area in module.subject_areas.all():
                if module.year not in real_years:
                    real_years.append(module.year)
        real_years.sort()
        subject_areas_real_years[subject_area] = real_years
    return render(
        request,
        'admin.html',
        {
            'main_admin': main_admin,
            'subject_areas': subject_areas,
            'subject_areas_real_years': subject_areas_real_years
        }
    )


@login_required
@user_passes_test(is_main_admin)
def main_settings(request):
    """Allows the Main Admin to set the basic settings"""
    if request.method == 'POST':
        form = MainSettingsForm(data=request.POST)
        if form.is_valid():
            current_year = form.cleaned_data['current_year']
            try:
                model = Setting.objects.get(name="current_year")
                model.value = current_year
                model.save()
            except Setting.DoesNotExist:
                Setting.objects.create(name="current_year", value=current_year)
            uni_name = form.cleaned_data['uni_name']
            try:
                model = Setting.objects.get(name="uni_name")
                model.value = uni_name
                model.save()
            except Setting.DoesNotExist:
                Setting.objects.create(name="uni_name", value=uni_name)
            uni_short_name = form.cleaned_data['uni_short_name']
            try:
                model = Setting.objects.get(name="uni_short_name")
                model.value = uni_short_name
                model.save()
            except Setting.DoesNotExist:
                Setting.objects.create(
                    name="uni_short_name", value=uni_short_name)
            nomosdb_url = form.cleaned_data['nomosdb_url']
            try:
                model = Setting.objects.get(name='nomosdb_url')
                model.value = nomosdb_url
                model.save()
            except Setting.DoesNotExist:
                Setting.objects.create(name='nomosdb_url', value=nomosdb_url)
            admin_name = form.cleaned_data['admin_name']
            try:
                model = Setting.objects.get(name='admin_name')
                model.value = admin_name
                model.save()
            except Setting.DoesNotExist:
                Setting.objects.create(name='admin_name', value=admin_name)
            admin_email = form.cleaned_data['admin_email']
            try:
                model = Setting.objects.get(name='admin_email')
                model.value = admin_email
                model.save()
            except Setting.DoesNotExist:
                Setting.objects.create(name='admin_email', value=admin_email)
            example_email = form.cleaned_data['example_email']
            try:
                model = Setting.objects.get(name='example_email')
                model.value = example_email
                model.save()
            except Setting.DoesNotExist:
                Setting.objects.create(
                    name='example_email', value='example_email')
        return redirect(reverse('home'))
    try:
        current_year = Setting.objects.get(name="current_year").value
    except Setting.DoesNotExist:
        current_year = str(datetime.date.today().year)
    try:
        uni_name = Setting.objects.get(name="uni_name").value
    except Setting.DoesNotExist:
        uni_name = 'Acme University'
    try:
        uni_short_name = Setting.objects.get(name="uni_short_name").value
    except Setting.DoesNotExist:
        uni_short_name = 'ACME U'
    try:
        nomosdb_url = Setting.objects.get(name="nomosdb_url").value
    except Setting.DoesNotExist:
        nomosdb_url = 'acme.nomosdb.org'
    try:
        admin_name = Setting.objects.get(name="admin_name").value
    except Setting.DoesNotExist:
        admin_name = "Chuck Jones"
    try:
        admin_email = Setting.objects.get(name="admin_email").value
    except Setting.DoesNotExist:
        admin_email = 'chuck.jones@acme.edu'
    try:
        example_email = Setting.objects.get(name="example_email").value
    except Setting.DoesNotExist:
        example_email = 'b.bunny23@acme.edu'
    form = MainSettingsForm(
        initial={
            'current_year': current_year,
            'uni_name': uni_name,
            'uni_short_name': uni_short_name,
            'nomosdb_url': nomosdb_url,
            'admin_name': admin_name,
            'admin_email': admin_email,
            'example_email': example_email,
        }
    )
    return render(request, 'main_settings_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def subject_areas(request):
    subject_areas = SubjectArea.objects.all()
    if request.method == 'POST':
        form = SubjectAreaForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('subject_areas'))
    form = SubjectAreaForm()
    return render(
        request,
        'subject_areas.html',
        {'subject_areas': subject_areas, 'form': form}
    )


@login_required
@user_passes_test(is_admin)
def course_overview(request):
    """Page that shows all courses"""
    courses = Course.objects.all()
    return render(request, 'course_overview.html', {'courses': courses})


@login_required
@user_passes_test(is_admin)
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
            return redirect(reverse('course_overview'))
    else:
        if edit:
            form = CourseForm(instance=course)
        else:
            form = CourseForm()
    return render(request, 'course_form.html', {'form': form, 'edit': edit})


@login_required
@user_passes_test(is_admin)
def add_or_edit_staff(request, username=None, testing=False):
    """Allows to edit or add a staff member.

    The classes concerned are the User class and the Staff class
    for additional details
    """
    if username:
        edit = True
        user = User.objects.get(username=username)
        staff = user.staff
    else:
        edit = False
    if request.method == 'POST':
        form = StaffForm(data=request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            if not edit:
                initials = ''
                for word in first_name.split():
                    initials += word[0]
                initials = initials[:3]
                initials += last_name[0]
                initials = initials.lower()
                number = 1
                still_searching = True
                while still_searching:
                    username = initials + str(number)
                    if User.objects.filter(username=username).exists():
                        number += 1
                    else:
                        still_searching = False
                password = User.objects.make_random_password()
                user = User.objects.create_user(username, email, password)
                message = new_staff_email(first_name, username, password)
                subject = 'NomosDB Login Data'
                sender = Setting.objects.get(name='admin_email').value
                if not testing:
                    send_mail(subject, message, sender, [email, ])
                else:
                    print('\n')
                    print('Subject: %s' % (subject,))
                    print('---')
                    print(message)
                staff = Staff.objects.create(user=user)
            for subject_area in staff.subject_areas.all():
                if subject_area.name not in form.cleaned_data['subject_areas']:
                    staff.subject_areas.remove(subject_area)
            for slug in form.cleaned_data['subject_areas']:
                subject_area = SubjectArea.objects.get(slug=slug)
                if subject_area not in staff.subject_areas.all():
                    staff.subject_areas.add(subject_area)
            staff.role = form.cleaned_data['role']
            staff.save()
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            return redirect(reverse('view_staff_by_name'))
    else:
        if edit:
            form = StaffForm(initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'subject_areas': SubjectArea.objects.all(),
                'role': staff.role
            })
        else:
            form = StaffForm(initial={'role': 'teacher'})
    return render(request, 'staff_form.html', {'form': form, 'edit': edit})


@login_required
@user_passes_test(is_admin)
def view_staff_by_subject(request):
    """Shows all staff members, sorted by subject"""
    subject_dict = {}
    for staff in Staff.objects.all():
        for subject_area in staff.subject_areas.all():
            if subject_area in subject_dict:
                subject_dict[subject_area].append(staff)
            else:
                subject_dict[subject_area] = [staff]
    return render(
        request, 'all_staff_by_subject.html', {'subject_dict': subject_dict})


@login_required
@user_passes_test(is_admin)
def view_staff_by_name(request):
    """Shows all staff members, sorted by name"""
    staff_members = Staff.objects.all()
    return render(
        request, 'all_staff_by_name.html', {'staff_members': staff_members})


@login_required
@user_passes_test(is_admin)
def delete_staff_member(request, username):
    """Deletes a staff member and the user belonging to it"""
    user = User.objects.get(username=username)
    staff = user.staff
    staff.delete()
    user.delete()
    return redirect('admin')


# Student related


@login_required
@user_passes_test(is_staff)
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
            if student.exam_id == '':  # Fixes problem with unique constraint
                student.exam_id = None
                student.save()
            return redirect(student.get_absolute_url())
    else:
        if edit:
            form = StudentForm(instance=student)
        else:
            form = StudentForm()
    return render(request, 'student_form.html', {'form': form, 'edit': edit})


@login_required
@user_passes_test(is_staff)
def student_view(request, student_id, meeting_id=None):
    """Shows all information about a student"""
    student = Student.objects.get(student_id=student_id)
    form = None
    meetings = None
    edit = False
    if student in request.user.staff.tutees.all():
        tutor = True
        allowed_to_see_notes = True
        if meeting_id:
            tutee_session = TuteeSession.objects.get(id=meeting_id)
            edit = meeting_id
        else:
            tutee_session = TuteeSession(
                tutee=student, tutor=request.user.staff)
        if request.method == "POST":
            form = TuteeSessionForm(instance=tutee_session, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect(student.get_absolute_url())
        else:
            form = TuteeSessionForm(instance=tutee_session)
    elif (request.user.staff.programme_director or
            request.user.staff.main_admin):
        tutor = False
        allowed_to_see_notes = True
    else:
        tutor = False
        allowed_to_see_notes = False
    if allowed_to_see_notes:
        meetings = TuteeSession.objects.filter(tutee=student)
    performances = {}
    for performance in student.performances.all():
        if performance.belongs_to_year in performances:
            performances[performance.belongs_to_year].append(performance)
        else:
            performances[performance.belongs_to_year] = [performance]
    return render(
        request,
        'student_view.html',
        {
            'student': student,
            'edit': edit,
            'form': form,
            'tutor': tutor,
            'meetings': meetings,
            'allowed_to_see_notes': allowed_to_see_notes,
            'performances': performances,
            'staff_pk': request.user.staff.pk
        }
    )


@login_required
@user_passes_test(is_staff)
def search_student(request):
    """Little search function. Can at some point be replaced with AJAX"""
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        students = []
        if len(q) > 1:
            if "," in q:
                search = q.split(",")
                first_name = search[-1].strip()
                last_name = search[0].strip()
            else:
                search = q.split()
                first_name = search[0]
                last_name = search[-1]
            students = Student.objects.filter(
                last_name__icontains=last_name,
                first_name__icontains=first_name
                )
        if len(students) == 0:
            students = Student.objects.filter(
                Q(last_name__istartswith=q) | Q(first_name__istartswith=q))
        if len(students) == 1:
            student = students[0]
            return redirect(student.get_absolute_url())
        else:
            return render(
                request,
                'search_results.html',
                {'students': students, 'query': q},
            )
    else:
        return redirect(reverse('home'))


@login_required
@user_passes_test(is_staff)
def year_view(request, year):
    """Shows all students in a particular year and allows bulk changes"""
    if request.method == 'POST':
        selected_students = request.POST.getlist('selected_student_id')
        selected_option = request.POST.__getitem__('modify')
        selected = selected_option.split('_')
        if selected[0] == 'tutor':
            tutor = User.objects.get(id=selected[1])
            for student_id in selected_students:
                student = Student.objects.get(student_id=student_id)
                student.tutor = tutor
                student.save()
        elif selected[0] == 'qld':
            if selected[1] == 'on':
                for student_id in selected_students:
                    student = Student.objects.get(student_id=student_id)
                    student.qld = True
                    student.save()
            elif selected[1] == 'off':
                for student_id in selected_students:
                    student = Student.objects.get(student_id=student_id)
                    student.qld = False
                    student.save()
        elif selected[0] == 'course':
            course = Course.objects.get(title=selected[1])
            for student_id in selected_students:
                student = Student.objects.get(student_id=student_id)
                student.course = course
                student.save()
        elif selected[0] == 'since':
            startyear = selected[1]
            for student_id in selected_students:
                student = Student.objects.get(student_id=student_id)
                student.since = startyear
                student.save()
        elif selected[0] == 'year':
            for student_id in selected_students:
                student = Student.objects.get(student_id=student_id)
                student.year = selected[1]
                student.save()
        elif selected[0] == 'active':
            if selected[1] == 'yes':
                for student_id in selected_students:
                    student = Student.objects.get(student_id=student_id)
                    student.active = True
                    student.save()
            elif selected[1] == 'no':
                for student_id in selected_students:
                    student = Student.objects.get(student_id=student_id)
                    student.active = False
                    student.save()
        elif selected[0] == 'delete':
            if selected[1] == 'yes':
                for student_id in selected_students:
                    student = Student.objects.get(student_id=student_id)
                    student.delete()
            if selected[1] == 'no':
                pass
        return redirect(reverse('year_view', args=[str(year)]))
    if year.startswith('imported_'):
        data = Data.objects.get(id=year)
        student_ids = data.value.split(',')
        students = Student.objects.filter(student_id__in=student_ids)
        headline = 'Recently Added Students'
        courses = Course.objects.all()
        show_year = True
    else:
        if request.user.staff.main_admin:
            if year == 'all':
                students = Student.objects.filter(active=True)
            elif year == 'unassigned':
                students = Student.objects.filter(year=None, active=True)
            elif year == 'inactive':
                students = Student.objects.filter(active=False)
            else:
                students = Student.objects.filter(year=year, active=True)
            courses = Course.objects.all()
        else:
            staff_subject_areas = (
                request.user.staff.subject_areas.all().values('name'))
            if year == 'all':
                students = Student.objects.filter(
                    active=True,
                    course__subject_areas__name__in=staff_subject_areas
                )
            elif year == 'unassigned':
                students = Student.objects.filter(
                    active=True,
                    course__subject_areas__name__in=staff_subject_areas,
                    year=None
                )
            elif year == 'inactive':
                students = Student.objects.filter(
                    active=False,
                    course__subject_areas__name__in=staff_subject_areas,
                )
            else:
                students = Student.objects.filter(
                    active=True,
                    course__subject_areas__name__in=staff_subject_areas,
                    year=year
                )
            courses = Course.objects.filter(
                subject_areas__name__in=staff_subject_areas)
        if year == 'all':
            headline = 'All Students'
            show_year = True
        elif year == 'unassigned':
            headline = 'Unassigned Students'
            show_year = True
        elif year == 'inactive':
            headline = 'Inactive Students'
            show_year = True
        elif year == '9':
            headline = 'Alumni'
            show_year = False
        elif year == '7':
            headline = 'Masters Students'
            show_year = False
        elif year == '8':
            headline = 'PhD Students'
            show_year = False
        else:
            headline = 'Year ' + year
            show_year = False
    academic_years = []
    current_year = int(Setting.objects.get(name='current_year').value)
    latest_start_year = current_year + 2
    for academic_year in ACADEMIC_YEARS:
        if academic_year[0] < latest_start_year:
            academic_years.append(academic_year[0])
    if is_admin(request.user):
        edit = True
    else:
        if request.user.staff.programme_director:
            edit = True
        else:
            edit = False
    number_of_students = len(students)
    return render(
        request,
        'year_view.html',
        {
            'students': students,
            'headline': headline,
            'show_year': show_year,
            'academic_years': academic_years,
            'courses': courses,
            'edit': edit,
            'number_of_students': number_of_students
        }
    )


@login_required
@user_passes_test(is_staff)
def assign_tutors(request, subject_area, year):
    """Allows admin or PD to assign tutees to tutors"""
    if is_admin(request.user) or request.user.staff.programme_director:
        subject_area = SubjectArea.objects.get(slug=subject_area)
        all_students = Student.objects.filter(active=True, year=int(year))
        students = []
        for student in all_students:
            if subject_area in student.course.subject_areas.all():
                students.append(student)

        if request.method == 'POST':
            for student in students:
                if student.student_id in request.POST:
                    if request.POST[student.student_id]:
                        user = User.objects.get(
                            username=request.POST[student.student_id])
                        student.tutor = user.staff
                        student.save()
                    else:
                        student.tutor = None
                        student.save()
            return redirect(reverse('admin'))

        else:

            all_teachers = Staff.objects.filter(role="teacher")
            teachers = []
            for teacher in all_teachers:
                if subject_area in teacher.subject_areas.all():
                    teacher_tpl = (
                        teacher.user.username,
                        teacher.name(),
                        teacher.tutees.count()
                    )
                    teachers.append(teacher_tpl)
            return render(
                request,
                'assign_tutors.html',
                {'students': students, 'teachers': teachers}
            )
    else:
        return redirect(reverse('home'))


@login_required
@user_passes_test(is_staff)
def all_attendances(request, subject_area, year):
    subject_area = SubjectArea.objects.get(slug=subject_area)
    all_students = Student.objects.filter(active=True, year=year)
    current_year = int(Setting.objects.get(name="current_year").value)
    rows = []
    weeks = WEEKS_TO_LOOK_AT
    admin_name = request.user.staff.name()
    for student in all_students:
        if subject_area in student.course.subject_areas.all():
            performances = Performance.objects.filter(
                student=student, module__year=current_year)
            problems = []
            attendances = []
            row = {}
            for performance in performances:
                if performance.missed_the_last_two_sessions():
                    attendancestr = performance.count_attendance()
                    attendancestr = attendancestr.replace('/', ' of ')
                    problems.append((performance.module.title, attendancestr))
                attendance = [performance.module.link()]
                attendance_dict = performance.attendance_as_dict()
                for week in weeks:
                    if str(week) in attendance_dict:
                        attendance.append(attendance_dict[str(week)])
                    else:
                        attendance.append('')
                attendances.append(attendance)
            row['student'] = student
            row['attendances'] = attendances
            if problems:
                row['message'] = attendance_email(
                    student, problems, admin_name)
            else:
                row['message'] = ''
            row['counter'] = (len(performances) + 1)
            rows.append(row)
    return render(
        request,
        'all_attendances.html',
        {
            'rows': rows,
            'subject_area': subject_area,
            'year': year,
            'weeks': weeks
        }
    )


@login_required
@user_passes_test(is_staff)
def delete_tutee_meeting(request, session_id):
    """Simply deletes a meeting record and returns to the student"""
    session_id = int(session_id)
    tutee_session = TuteeSession.objects.get(id=session_id)
    if (
            request.user.staff == tutee_session.tutor or
            request.user.staff.main_admin
    ):
        student = tutee_session.tutee
        tutee_session.delete()
    return redirect(student.get_absolute_url())


@login_required
@user_passes_test(is_staff)
def my_tutees(request):
    staff = request.user.staff
    tutees = Student.objects.filter(tutor=staff)
    email_addresses = ''
    no_email_addresses = []
    rows = []
    for tutee in tutees:
        row = {}
        if tutee.email:
            email_addresses += tutee.email + ";"
        else:
            name = tutee.first_name + " " + tutee.last_name
            no_email_addresses.append(name)
        row['student'] = tutee
        if not tutee.active:
            row['inactive'] = True
        current_year = int(Setting.objects.get(name="current_year").value)
        performances = Performance.objects.filter(
            student=tutee, module__year=current_year)
        problems = []
        for performance in performances:
            attendance = performance.count_attendance()
            attendance_lst = attendance.split('/')
            present = int(attendance_lst[0])
            sessions = int(attendance_lst[1])
            if present != 0:
                factor = sessions / present
                if factor > 1.5:
                    problems.append(
                        "Missed more than a third of the sessions in %s" % (
                            performance.module.title)
                    )
            else:
                if sessions == 1:
                    problems.append('Missed the first session in %s' % (
                        performance.module.title)
                    )
                elif sessions > 1:
                    problems.append('Missed all sessions in %s' % (
                        performance.module.title)
                    )
            result_tpls = performance.all_assessment_results_as_tpls(
                only_result=True)
            for tpl in result_tpls:
                if tpl[1]:
                    if tpl[1] < 40:
                        problems.append('Failed %s for %s (%s)' % (
                            tpl[0], module, tpl[1])
                        )
        row['problems'] = problems
        row['meetings'] = TuteeSession.objects.filter(tutee=tutee)
        rows.append(row)
    return render(
        request,
        'my_tutees.html',
        {
            'rows': rows,
            'email_addresses': email_addresses,
            'no_email_addresses': no_email_addresses,
        }
    )


@login_required
@user_passes_test(is_pd)
def all_tutee_meetings(request, subject_area, year):
    subject_area = SubjectArea.objects.get(slug=subject_area)
    all_students = Student.objects.filter(active=True, year=year)
    students = []
    for student in all_students:
        if subject_area in student.course.subject_areas.all():
            students.append(student)
    rows = []
    max_columns = 0
    for student in students:
        meetings = TuteeSession.objects.filter(tutee=student).count()
        if meetings > max_columns:
            max_columns = meetings
    for student in students:
        row = {}
        row['student'] = student
        sessions = TuteeSession.objects.filter(tutee=student)
        row['sessions'] = []
        for counter in range(0, max_columns):
            try:
                row['sessions'].append(sessions[counter])
            except IndexError:
                row['sessions'].append(None)
        rows.append(row)
    return render(
        request,
        'all_tutees.html',
        {
            'max_columns': max_columns,
            'year': year,
            'subject_area': subject_area,
            'rows': rows
        }
    )


# Module views


@login_required
@user_passes_test(is_staff)
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
            initial = {}
            if request.user.staff.subject_areas:
                list_of_subject_areas = []
                for subject_area in request.user.staff.subject_areas.all():
                    list_of_subject_areas.append(subject_area.pk)
                initial['subject_areas'] = list_of_subject_areas
            if request.user.staff.role == 'teacher':
                initial['teachers'] = [request.user.staff.pk]
            form = ModuleForm(initial=initial)
    if TEACHING_WEEK_OPTIONS:  # Ugly, but it works fine...
        javascript = '<script type="text/javascript">'
        javascript += '$(document).ready(function(){'
        for number in TEACHING_WEEK_OPTIONS:
            javascript += '$("#option_' + str(number) + '").click(function(){'
            javascript += '$("#id_first_session").val("'
            javascript += TEACHING_WEEK_OPTIONS[number][1]
            javascript += '");'
            javascript += '$("#id_last_session").val("'
            javascript += TEACHING_WEEK_OPTIONS[number][2]
            javascript += '");'
            javascript += '$("#id_no_teaching_in").val("'
            javascript += TEACHING_WEEK_OPTIONS[number][3]
            javascript += '");'
            javascript += '});'
        javascript += '});'
        javascript += '</script>'
    else:
        javascript = ''
    return render(
        request,
        'module_form.html',
        {'form': form, 'edit': edit, 'javascript': javascript}
    )


@login_required
@user_passes_test(is_staff)
def module_view(request, code, year):
    """Shows all information about a module"""
    module = Module.objects.get(code=code, year=year)
    performances = Performance.objects.filter(
        module=module, student__active=True)
    seminar_groups = []
    for performance in performances:
        if performance.seminar_group:
            if performance.seminar_group not in seminar_groups:
                seminar_groups.append(performance.seminar_group)
    seminar_groups.sort()
    seminar_group_links = []
    for seminar_group in seminar_groups:
        seminar_group_links.append(
            (seminar_group, module.get_attendance_url(seminar_group))
        )
    seminar_group_links.append(
        ('all', module.get_attendance_url('all'))
    )
    if request.user.staff in module.teachers.all():
        admin_or_instructor = True
    elif request.user.staff.role == 'admin':
        admin_or_instructor = True
    else:
        admin_or_instructor = False
    return render(
        request,
        'module_view.html',
        {
            'module': module,
            'performances': performances,
            'seminar_group_links': seminar_group_links,
            'admin_or_instructor': admin_or_instructor,
        }
    )


@login_required
@user_passes_test(is_staff)
def add_students_to_module(request, code, year):
    """Simple form to add students to a module and create Performance items"""
    module = Module.objects.get(code=code, year=year)
    current_year = int(Setting.objects.get(name="current_year").value)
    if request.method == 'POST':
        students_to_add = request.POST.getlist('student_ids')
        for student_id in students_to_add:
            student = Student.objects.get(student_id=student_id)
            student.modules.add(module)
            student.save()
            time_difference = current_year - module.year
            belongs_to = student.year - time_difference
            Performance.objects.create(
                module=module, student=student, belongs_to_year=belongs_to)
        return redirect(module.get_absolute_url())
    students_in_module = module.students.all()
    if len(module.eligible) > 1:
        more_than_one_year = True
    else:
        more_than_one_year = False
    students = []
    years = []
    for number in module.eligible:
        year = int(number)
        time_difference = module.year - current_year
        year = year - time_difference
        years.append(year)
        students_this_year = Student.objects.filter(year=year, active=True)
        for student in students_this_year:
            if student not in students_in_module:
                for subject_area in module.subject_areas.all():
                    if subject_area in student.course.subject_areas.all():
                        if student not in students:
                            students.append(student)
    courses = {}
    for student in students:
        if student.course.short_title in courses:
            courses[student.course.short_title].append(student.student_id)
        else:
            courses[student.course.short_title] = [student.student_id]
    return render(
        request,
        'add_students_to_module.html',
        {'module': module, 'students': students, 'courses': courses}
    )


@login_required
@user_passes_test(is_staff)
def remove_student_from_module(request, code, year, student_id):
    """Removes student from module, deletes performance object"""
    module = Module.objects.get(code=code, year=year)
    student = Student.objects.get(student_id=student_id)
    performance = Performance.objects.get(module=module, student=student)
    performance.delete()
    student.modules.remove(module)
    return redirect(module.get_absolute_url())


@login_required
@user_passes_test(is_staff)
def delete_module(request, code, year):
    """Deletes a module and related performances, assessments and results"""
    module = Module.objects.get(code=code, year=year)
    if is_admin(request.user) or request.user.staff in module.teachers.all():
        module.delete()
        return redirect(reverse('home'))
    else:
        return redirect(module.get_absolute_url())


@login_required
@user_passes_test(is_staff)
def assign_seminar_groups(request, code, year):
    """Allows to assign the students to seminar groups graphically"""
    module = Module.objects.get(code=code, year=year)
    students = module.students.all()
    if request.method == 'POST':
        save_these = True
        randomize = False
        randomize_all = False
        if 'action' in request.POST:
            if request.POST['action'] == 'Go':
                randomize = True
                if 'ignore' in request.POST:
                    save_these = False
                    randomize_all = True
        if save_these:
            for student in students:
                if student.student_id in request.POST:
                    tmp = request.POST[student.student_id]
                    group = int(tmp)
                    performance = Performance.objects.get(
                        student=student, module=module)
                    if group == 0:
                        performance.seminar_group = None
                    else:
                        performance.seminar_group = group
                    performance.save()
        if randomize:
            number_of_groups = int(request.POST['number_of_groups'])
            already_existing_groups = 0
            all_performances = Performance.objects.filter(module=module)
            for performance in all_performances:
                if performance.seminar_group:
                    if performance.seminar_group > already_existing_groups:
                        already_existing_groups = performance.seminar_group
            if already_existing_groups > number_of_groups:
                number_of_groups = already_existing_groups
            number_of_students = len(students)
            s_p_g = number_of_students / number_of_groups
            max_students_per_group = int(s_p_g)
            if s_p_g > max_students_per_group:
                max_students_per_group += 1
            group_members = {}
            for i in range(1, number_of_groups+1):
                group_members[i] = 0
            performances_to_randomize = []
            for student in students:
                performance = Performance.objects.get(
                    student=student, module=module)
                if randomize_all:
                    performances_to_randomize.append(performance)
                else:
                    if performance.seminar_group is None:
                        performances_to_randomize.append(performance)
                    else:
                        group_members[performance.seminar_group] += 1
            shuffle(performances_to_randomize)
            for performance in performances_to_randomize:
                for number in group_members:
                    if group_members[number] < max_students_per_group:
                        performance.seminar_group = number
                        performance.save()
                        group_members[number] += 1
                        break
            return redirect(module.get_seminar_groups_url())
        return redirect(module.get_absolute_url())
    dictionary = {}
    for student in students:
        performance = Performance.objects.get(student=student, module=module)
        if performance.seminar_group is None:
            group = "0"
        else:
            group = str(performance.seminar_group)
        if group in dictionary:
            dictionary[group].append(performance)
        else:
            dictionary[group] = [performance]
    no_of_students = len(students)
    mg = no_of_students / 2
    max_groups = int(mg)
    if mg > max_groups:
        max_groups += 1
    groups = []
    for i in range(1, max_groups+1):
        ms = no_of_students / i
        max_students = int(ms)
        if ms > max_students:
            max_students += 1
        groups.append((i, max_students))
    return render(
        request,
        'seminar_groups.html',
        {
            'module': module,
            'dictionary': dictionary,
            'max_groups': max_groups,
            'groups': groups
        }
    )


@login_required
@user_passes_test(is_staff)
def assign_seminar_groups_old_browser(request, code, year):
    """Older Form to assign seminar groups

    the drag and drop variant does not work on IE
    """
    module = Module.objects.get(code=code, year=year)
    students = module.students.all()
    performances = []
    for student in students:
        performance = Performance.objects.get(student=student, module=module)
        performances.append(performance)
    random_options = {}
    for i in range(1, 10):
        # Up to 10 Seminar groups. Create a dictionary that lists the options
        # and the maximum number of students per group
        all = len(students)
        number = all / i
        left = all % i
        if left > 0:
            number = number + 1
        random_options[i] = round(number)

    if request.method == 'POST':
        for student in students:
            if student.student_id in request.POST:
                tmp = request.POST[student.student_id]
                try:
                    seminar_group = int(tmp)
                    if seminar_group in range(0, 99):
                        performance = Performance.objects.get(
                            student=student, module=module)
                        performance.seminar_group = seminar_group
                        performance.save()
                except ValueError:
                        pass
        return redirect(module.get_absolute_url())
    return render(
        request,
        'old_seminar_groups.html',
        {
            'module': module,
            'performances': performances,
            'random_options': random_options
        },
    )


@login_required
@user_passes_test(is_staff)
def assign_assessment_groups(request, code, year, slug, attempt):
    """Allows to assign the students to seminar groups graphically"""
    module = Module.objects.get(code=code, year=year)
    students = module.students.all()
    assessment = Assessment.objects.get(module=module, slug=slug)
    if request.method == 'POST':
        save_these = True
        randomize = False
        randomize_all = False
        if 'action' in request.POST:
            if request.POST['action'] == 'Go':
                randomize = True
                if 'ignore' in request.POST:
                    save_these = False
                    randomize_all = True
        if save_these:
            for student in students:
                if student.student_id in request.POST:
                    tmp = request.POST[student.student_id]
                    group = int(tmp)
                    performance = Performance.objects.get(
                        student=student, module=module)
                    try:
                        result = AssessmentResult.objects.get(
                            part_of=performance, assessment=assessment)
                    except AssessmentResult.DoesNotExist:
                        result = performance.assessment_results.create(
                            assessment=assessment)
                    if attempt == 'first':
                        if group == 0:
                            result.set_assessment_group(None)
                        else:
                            result.set_assessment_group(group)
                    else:
                        if group == 0:
                            result.set_assessment_group(None, 'resit')
                        else:
                            result.set_assessment_group(group, 'resit')
        if randomize:
            number_of_groups = int(request.POST['number_of_groups'])
            already_existing_groups = 0
            all_performances = Performance.objects.filter(module=module)
            for performance in all_performances:
                try:
                    result = AssessmentResult.objects.get(
                        part_of=performance, assessment=assessment)
                except AssessmentResult.DoesNotExist:
                    result = performance.assessment_results.create(
                        assessment=assessment)
                if attempt == 'first':
                    this_group = result.assessment_group
                else:
                    this_group = result.resit_assessment_group
                if this_group:
                    if this_group > already_existing_groups:
                        already_existing_groups = this_group
            if already_existing_groups > number_of_groups:
                number_of_groups = already_existing_groups
            number_of_students = len(students)
            s_p_g = number_of_students / number_of_groups
            max_students_per_group = int(s_p_g)
            if s_p_g > max_students_per_group:
                max_students_per_group += 1
            group_members = {}
            for i in range(1, number_of_groups+1):
                group_members[i] = 0
            performances_to_randomize = []
            for student in students:
                performance = Performance.objects.get(
                    student=student, module=module)
                if randomize_all:
                    performances_to_randomize.append(performance)
                else:
                    try:
                        result = AssessmentResult.objects.get(
                            part_of=performance, assessment=assessment)
                    except AssessmentResult.DoesNotExist:
                        result = performance.assessment_results.create(
                            assessment=assessment)
                    if result.assessment_group is None:
                        performances_to_randomize.append(performance)
                    else:
                        group_members[result.assessment_group] += 1
            shuffle(performances_to_randomize)
            for performance in performances_to_randomize:
                try:
                    result = AssessmentResult.objects.get(
                        part_of=performance, assessment=assessment)
                except AssessmentResult.DoesNotExist:
                    result = performance.assessment_results.create(
                        assessment=assessment)
                for number in group_members:
                    if group_members[number] < max_students_per_group:
                        if attempt == 'first':
                            result.set_assessment_group(number)
                        group_members[number] += 1
                        break
            if attempt == 'first':
                return redirect(assessment.get_assessment_groups_url())
            else:
                return redirect(assessment.get_assessment_groups_url('resit'))
        return redirect(module.get_absolute_url())

    dictionary = {}
    for student in students:
        performance = Performance.objects.get(student=student, module=module)
        try:
            result = AssessmentResult.objects.get(
                part_of=performance, assessment=assessment)
        except AssessmentResult.DoesNotExist:
            result = performance.assessment_results.create(
                assessment=assessment)
        if attempt == 'first':
            if result.assessment_group is None:
                group = "0"
            else:
                group = str(result.assessment_group)
        else:
            if result.resit_assessment_group is None:
                group = "0"
            else:
                group = str(result.resit_assessment_group)
        if group in dictionary:
            dictionary[group].append(performance)
        else:
            dictionary[group] = [performance]
    no_of_students = len(students)
    mg = no_of_students / 2
    max_groups = int(mg)
    if mg > max_groups:
        max_groups += 1
    groups = []
    for i in range(1, max_groups+1):
        ms = no_of_students / i
        max_students = int(ms)
        if ms > max_students:
            max_students += 1
        groups.append((i, max_students))
    return render(
        request,
        'assessment_groups.html',
        {
            'module': module,
            'dictionary': dictionary,
            'max_groups': max_groups,
            'groups': groups,
            'assessment': assessment.title
        }
    )


@login_required
@user_passes_test(is_staff)
def attendance(request, code, year, group):
    """The registers for the seminar groups or the whole module"""
    module = Module.objects.get(code=code, year=year)
    group = str(group)
    if group == 'all':
        performances = Performance.objects.filter(module=module)
        seminar_group = False
    else:
        performances = Performance.objects.filter(
            module=module,
            seminar_group=group
        )
        seminar_group = group
    if request.method == 'POST':
        save = request.POST['save']
        save_li = save.split()
        check = 'all'
        for word in save_li:
            if word.isdigit():
                check = word
        for performance in performances:
            student_id = performance.student.student_id
            for week in module.all_teaching_weeks():
                week = str(week)
                key = student_id + '_' + week
                if key in request.POST:
                    presence = request.POST[key]
                    if check == 'all':
                        performance.save_attendance(week, presence)
                    else:
                        if week == check:
                            performance.save_attendance(week, presence)
        return redirect(module.get_absolute_url())
    this_week = week_number()
    return render(
        request,
        'attendance.html',
        {
            'seminar_group': seminar_group,
            'performances': performances,
            'module': module,
            'this_week': this_week
        }
    )


@login_required
@user_passes_test(is_staff)
def assessment(request, code, year, slug=None):
    """Enter and edit the assessments for each module"""
    module = Module.objects.get(code=code, year=year)
    assessments = list(module.assessments.all())
    if slug:
        assessment = Assessment.objects.get(module=module, slug=slug)
        assessments.remove(assessment)
        edit = assessment.title
    else:
        edit = False
    if request.method == 'POST':
        if edit:
            form = AssessmentForm(instance=assessment, data=request.POST)
        else:
            form = AssessmentForm(data=request.POST)
        if form.is_valid():
            assessment = form.save()
            assessment.module = module
            assessment.save()
            return redirect(module.get_assessment_url())
    else:
        if edit:
            form = AssessmentForm(instance=assessment)
        else:
            form = AssessmentForm()
    value_so_far = 0
    for assessment in assessments:
        value_so_far += assessment.value
    value_left = 100 - value_so_far

    return render(
        request,
        'assessment.html',
        {
            'form': form,
            'edit': edit,
            'module': module,
            'assessments': assessments,
            'value_left': value_left
        }
    )


@login_required
@user_passes_test(is_staff)
def delete_assessment(request, code, year, slug):
    """Deletes an assessment and all connected results.

    The confirmation is done with JQuery"""
    module = Module.objects.get(code=code, year=year)
    assessment = Assessment.objects.get(module=module, slug=slug)
    results = AssessmentResult.objects.filter(assessment=assessment)
    for result in results:
        result.delete()
    assessment.delete()
    return redirect(module.get_assessment_url())


def toggle_assessment_availability(request, code, year, slug, attempt):
    """Makes feedback available to students"""
    module = Module.objects.get(code=code, year=year)
    assessment = Assessment.objects.get(module=module, slug=slug)
    if attempt == 'first':
        if assessment.available:
            assessment.available = False
        else:
            assessment.available = True
    elif attempt == 'resit':
        if assessment.resit_available:
            assessment.resit_available = False
        else:
            assessment.resit_available = True
    elif attempt == 'qld_resit':
        if assessment.qld_resit_available:
            assessment.qld_resit_available = False
        else:
            assessment.qld_resit_available = True
    else:
        if assessment.second_resit_available:
            assessment.second_resit_available = False
        else:
            assessment.second_resit_available = True
    assessment.save()
    return redirect(module.get_absolute_url())


@login_required
@user_passes_test(is_staff)
def seminar_group_overview(request, code, year):
    """Gives a nice overview of seminar groups"""
    module = Module.objects.get(code=code, year=year)
    performances = Performance.objects.filter(module=module)
    seminar_groups = {}
    for performance in performances:
        if performance.seminar_group in seminar_groups:
            seminar_groups[performance.seminar_group].append(
                performance.student.short_name()
            )
        else:
            seminar_groups[performance.seminar_group] = [
                performance.student.short_name()
            ]
    for group in seminar_groups:
        seminar_groups[group].sort()
    return render(
        request,
        'seminar_group_overview.html',
        {'seminar_groups': seminar_groups, 'module': module}
    )


@login_required
@user_passes_test(is_staff)
def assessment_group_overview(request, code, year, slug, attempt):
    """Gives a nice overview of assessment groups"""
    module = Module.objects.get(code=code, year=year)
    performances = Performance.objects.filter(module=module)
    assessment = Assessment.objects.get(module=module, slug=slug)
    assessment_groups = {}
    for performance in performances:
        try:
            result = AssessmentResult.objects.get(
                assessment=assessment, part_of=performance)
        except AssessmentResult.DoesNotExist:
            result = performance.assessment_results.create(
                assessment=assessment)
        if attempt == 'first':
            group = result.assessment_group
        else:
            group = result.resit_assessment_group
        if group in assessment_groups:
            assessment_groups[group].append(
                performance.student.short_name()
            )
        else:
            assessment_groups[group] = [
                performance.student.short_name()
            ]
    for group in assessment_groups:
        assessment_groups[group].sort()
    return render(
        request,
        'assessment_group_overview.html',
        {
            'assessment_groups': assessment_groups,
            'module': module,
            'assessment': assessment
        }
    )


# Data import / export


@login_required
@user_passes_test(is_staff)
def upload_csv(request):
    """Upload CSV, saves result in session and redirects to parser"""
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['csvfile']
            f.read()
            csv_string = ''
            for line in f:
                csv_string += line.decode('utf-8') + '/////'
            chars = ascii_letters + digits
            data_id = ''
            while data_id == '':
                data_id = ''.join(choice(chars) for x in range(16))
                try:
                    Data.objects.create(id=data_id, value=csv_string)
                except IntegrityError:
                    data_id = ''
            return redirect(reverse('parse_csv', args=[data_id]))
    else:
        form = CSVUploadForm()
    return render(request, 'upload_csv.html', {'form': form})


@login_required
@user_passes_test(is_staff)
def parse_csv(request, data_id):
    """Parses CSV Files with Student data, creates / amends Students"""
    data = Data.objects.get(id=data_id)
    importdata = data.value.split('/////')
    table = []
    no_of_columns = 0
    for line in importdata:
        row = line.split(';')
        if len(row) > no_of_columns:
            no_of_columns = len(row)
        table.append(row)
    if request.method == "POST":
        all_ids = ''
        list_of_columns = []
        i = 1
        while i <= no_of_columns:
            column = 'column' + str(i)
            list_of_columns.append(request.POST[column])
            i += 1
        item_in_table = 0
        ignore_students = request.POST.getlist('exclude')
        for row in table:
            item_in_table += 1
            if str(item_in_table) not in ignore_students:
                result = {}
                counter = 0
                for entry in row:
                    column = list_of_columns[counter]
                    if column != 'ignore':
                        result[column] = entry
                    counter += 1
                try:
                    student = Student.objects.get(
                        student_id=result['student_id']
                    )
                except Student.DoesNotExist:
                    student = Student.objects.create(
                        student_id=result['student_id']
                    )
                if 'first_name' in result:
                    student.first_name = result['first_name']
                if 'last_name' in result:
                    student.last_name = result['last_name']
                if 'since' in result:
                    student.since = int(result['since'])
                if 'year' in result:
                    # Can contain other entries, so necessary to parse
                    possible_years = ['1', '2', '3', '7', '8', '9']
                    tmp = result['year'].split()
                    for part in tmp:
                        if part in possible_years:
                            student.year = int(part)
                            break
                if 'email' in result:
                    student.email = result['email']
                if 'phone_number' in result:
                    number = ''
                    if result['phone_number'][0] not in ['0', '+']:
                        number = '0' + result['phone_number']
                    else:
                        number = result['phone_number']
                    student.phone_number = number
                if 'cell_number' in result:
                    number = ''
                    if not result['cell_number'].startswith('0'):
                        number = '0' + result['cell_number']
                    else:
                        number = result['cell_number']
                    student.cell_number = number
                if 'permanent_email' in result:
                    student.permanent_email = result['permanent_email']
                if 'achieved_degree' in result:
                    student.achieved_degree = result['achieved_degree']
                address_fields = [
                    'address1'
                    'address2',
                    'address3',
                    'address4',
                    'address5'
                ]
                if any(k in result for k in address_fields):
                    student.address = ""
                    for field in address_fields:
                        if field in result:
                            student.address += result[field] + '\n'
                home_address_fields = [
                    'home_address1'
                    'home_address2',
                    'home_address3',
                    'home_address4',
                    'home_address5'
                ]
                if any(k in result for k in home_address_fields):
                    student.home_address = ''
                    for field in home_address_fields:
                        if field in result:
                            student.home_address += result[field] + '\n'
                all_ids += student.student_id + ','
                student.save()
        chars = ascii_letters + digits
        data_id = 'imported_'
        while data_id == 'imported_':
            random_string = ''.join(choice(chars) for x in range(8))
            data_id += random_string
            try:
                Data.objects.create(id=data_id, value=all_ids)
            except IntegrityError:
                data_id = 'imported_'
        return redirect(reverse('year_view', args=[data_id]))
    options = (
        ('student_id', 'Student ID'),
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('exam_id', 'Exam ID'),
        ('since', 'Studying since'),
        ('year', 'Year of Study'),
        ('email', 'University email'),
        ('phone_number', 'Phone Number'),
        ('cell_number', 'Mobile Number'),
        ('permanent_email', 'Private email'),
        ('achieved_degree', 'Achieved degree'),
        ('address1', 'Term time address line 1'),
        ('address2', 'Term time address line 2'),
        ('address3', 'Term time address line 3'),
        ('address4', 'Term time address line 4'),
        ('address5', 'Term time address line 5'),
        ('home_address1', 'Home address line 1'),
        ('home_address2', 'Home address line 2'),
        ('home_address3', 'Home address line 3'),
        ('home_address4', 'Home address line 4'),
        ('home_address5', 'Home address line 5')
    )
    return render(
        request,
        'parse_csv.html',
        {
            'columns': no_of_columns,
            'csv_list': table,
            'options': options
        }
    )


@login_required
@user_passes_test(is_staff)
def export_attendance_sheet(request, code, year):
    """Returns attendance sheets for a module."""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment; filename=attendance_sheet.pdf')
    document = SimpleDocTemplate(response)
    elements = []
    module = Module.objects.get(code=code, year=year)
    styles = getSampleStyleSheet()
    heading = module.__str__()
    performances = Performance.objects.filter(module=module)
    no_of_seminar_groups = 0
    for performance in performances:
        if performance.seminar_group > no_of_seminar_groups:
            no_of_seminar_groups = performance.seminar_group
    counter = 0
    while counter < no_of_seminar_groups:
        counter += 1
        subheading = "Seminar Group " + str(counter)
        elements.append(Paragraph(heading, styles['Heading1']))
        elements.append(Paragraph(subheading, styles['Heading2']))
        elements.append(Spacer(1, 20))
        data = []
        header = ['Name']
        column = 0
        last_week = module.last_session + 1
        if module.no_teaching_in:
            no_teaching = module.no_teaching_in.split(",")
        else:
            no_teaching = []
        weeklist = []
        for week in range(module.first_session, last_week):
            strweek = str(week)
            if strweek not in no_teaching:
                header.append(strweek)
                weeklist.append(strweek)
        data.append(header)
        performances = Performance.objects.filter(
            module=module, seminar_group=counter)
        for performance in performances:
            attendance = performance.attendance_as_dict()
            row = [performance.student]
            for week in weeklist:
                if week in attendance:
                    if attendance[week] == 'p':
                        row.append(u'\u2713')
                    elif attendance[week] == 'e':
                        row.append('e')
                    elif attendance[week] == 'a':
                        row.append('-')
                else:
                    row.append(' ')
            data.append(row)
        table = Table(data)
        table.setStyle(
            TableStyle([
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]
            )
        )
        elements.append(table)
        elements.append(PageBreak())
    document.build(elements)
    return response


@login_required
@user_passes_test(is_admin)
def export_tier_4_attendance(request, slug, year):
    """Gives a pdf listing the attendance of all Tier 4 students"""
    subject_area = SubjectArea.objects.get(slug=slug)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment; filename=tier_4_attendance_' +
        slug +
        '_' +
        year +
        '.pdf'
    )
    document = SimpleDocTemplate(response)
    elements = []
    styles = getSampleStyleSheet()
    next_year = str(int(year) + 1)
    ac_year = year + '/' + next_year[-2:]
    heading = 'Tier 4 Attendance ' + subject_area.name + ' ' + ac_year
    elements.append(Paragraph(heading, styles['Heading1']))
    all_students = Student.objects.filter(active=True, tier_4=True)
    students = []
    for student in all_students:
        if subject_area in student.course.subject_areas.all():
            students.append(student)
    for student in students:
        print(student.name())
        modules = {}
        performances = Performance.objects.filter(
            student=student,
            module__year=int(year)
        )
        all_weeks = []
        all_modules = []
        weeks = {}
        for performance in performances:
            if performance.module.title not in all_modules:
                all_modules.append(performance.module.title)
            attendance_dict = performance.attendance_as_dict()
            for key, value in attendance_dict.items():
                if key not in all_weeks:
                    all_weeks.append(key)
                if key in weeks:
                    weeks[key][performance.module.title] = value
                else:
                    weeks[key] = {performance.module.title: value}
        all_weeks.sort()
        all_modules.sort()
        elements.append(Paragraph(student.name(), styles['Heading2']))
        data = []
        top_line = ['', 'Week starting']
        for x in range(1, len(all_weeks)):
            top_line.append('')
        data.append(top_line)
        header = ['Module']
        for week in all_weeks:
            starting_date = week_starting_date(week, year)
            print_date = (
                str(starting_date.day) +
                '/' +
                str(starting_date.month) +
                '/' +
                str(starting_date.year)
            )
            header.append(print_date)
        data.append(header)
        for module_title in all_modules:
            row = [module_title]
            for week in all_weeks:
                if module_title in weeks[week]:
                    if weeks[week][module_title] in ['p', 'e']:
                        row.append(u'\u2713')
                    else:
                        row.append('-')
                else:
                    row.append(' ')
            data.append(row)
        table = Table(data)
        table.setStyle(
            TableStyle([
                ('SPAN', (1, 0), (-1, 0)),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BACKGROUND', (0, 0), (-1, 1), colors.lightgrey),
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]
            )
        )
        elements.append(table)
    document.build(elements)
    return response
