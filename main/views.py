from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from main.forms import *
from main.functions import week_number
from main.messages import new_staff_email
from main.models import *
from main.unisettings import *
from random import shuffle, choice
from string import ascii_letters, digits
from django.core.urlresolvers import resolve


def is_teacher(user):
    if hasattr(user, 'staff'):
        if user.staff.role == 'teacher':
            return True
    return False


def is_admin(user):
    if hasattr(user, 'staff'):
        if user.staff.role == 'admin':
            return True
    return False


def is_staff(user):
    if hasattr(user, 'staff'):
        return True
    else:
        return False


@login_required
def home(request):
    """Simply the home page, nothing there yet"""
    # use if to show different pages for students and teachers!
    return render(request, 'home.html', {})


@login_required
@user_passes_test(is_admin)
def admin(request):
    """Opens the admin dashboard"""
    return render(request, 'admin.html', {})


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
def student_view(request, student_id):
    """Shows all information about a student"""
    student = Student.objects.get(student_id=student_id)
    return render(request, 'student_view.html', {'student': student})


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
            list_of_subject_areas = []
            if request.user.staff.subject_areas:
                for subject_area in request.user.staff.subject_areas:
                    list_of_subject_areas.append(subject_area.pk)
            form = ModuleForm(
                initial={'subject_areas': list_of_subject_areas})
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
    return render(
        request,
        'module_view.html',
        {
            'module': module,
            'performances': performances,
            'seminar_group_links': seminar_group_links
        }
    )


@login_required
@user_passes_test(is_staff)
def add_students_to_module(request, code, year):
    """Simple form to add students to a module and create Performance items"""
    module = Module.objects.get(code=code, year=year)
    if request.method == 'POST':
        students_to_add = request.POST.getlist('student_ids')
        for student_id in students_to_add:
            student = Student.objects.get(student_id=student_id)
            student.modules.add(module)
            student.save()
            Performance.objects.create(module=module, student=student)
        return redirect(module.get_absolute_url())
    students_in_module = module.student_set.all()
    if len(module.eligible) > 1:
        more_than_one_year = True
    else:
        more_than_one_year = False
    students = []
    years = []
    for number in module.eligible:
        year = int(number)
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
def assign_seminar_groups(request, code, year):
    """Allows to assign the students to seminar groups graphically"""
    module = Module.objects.get(code=code, year=year)
    students = module.student_set.all()
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
            form = AssessmentForm(instance=module, data=request.POST)
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
@user_passes_test(is_admin)
def add_or_edit_staff(request, username=None):
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
                # send_mail(
                #   '%s Login Data' % (NOMOSDB_NAME)
                #   message,
                #   ADMIN_EMAIL,
                #   [email, ]
                # )
                print(message)
                staff = Staff.objects.create(user=user)
            for subject_area in staff.subject_areas.all():
                if subject_area.name not in form.cleaned_data['subject_areas']:
                    staff.subject_areas.remove(subject_area)
            for name in form.cleaned_data['subject_areas']:
                subject_area = SubjectArea.objects.get(name=name)
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
            print(form.errors)
    else:
        if edit:
            form = StaffForm(initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'subject_areas': staff.subject_areas.all(),
                'role': staff.role
            })
        else:
            form = StaffForm(initial={'role': 'teacher'})
    return render(request, 'staff_form.html', {'form': form, 'edit': edit})


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
    current_year = int(Settings.objects.get(name='current_year').value)
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
    return render(
        request,
        'year_view.html',
        {
            'students': students,
            'headline': headline,
            'show_year': show_year,
            'academic_years': academic_years,
            'courses': courses,
            'edit': edit
        }
    )


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
        row = line.split(',')
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
                if 'phone_no' in result:
                    student.phone_number = result['phone_no']
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
        ('phone_no', 'Phone Number'),
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
def import_success(request):
    """Displays successful upload / parsing"""
    successful_entrys = request.session.get('number_of_imports')
    return render(request, 'import_success.html', {successful_entries})
