from datetime import datetime
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from feedback.forms import *
from feedback.models import *
from main.models import *
from main.views import is_staff, is_student
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph, Spacer, Image, Table, TableStyle, SimpleDocTemplate
)
from reportlab.platypus.flowables import PageBreak

# Forms for entering feedback


def na(request):
    return render(request, 'na.html', {})


def individual_feedback(
        request, code, year, assessment_slug, student_id, attempt='first'):
    """The form for all marksheets concerning just one student"""
    module = Module.objects.get(code=code, year=year)
    assessment = Assessment.objects.get(module=module, slug=assessment_slug)
    student = Student.objects.get(student_id=student_id)
    performance = Performance.objects.get(module=module, student=student)
    try:
        assessment_result = AssessmentResult.objects.get(
            assessment=assessment, part_of=performance)
    except AssessmentResult.DoesNotExist:
        assessment_result = AssessmentResult.objects.create(
            assessment=assessment)
        performance.assessment_results.add(assessment_result)
        performance.save()
    try:
        feedback = IndividualFeedback.objects.get(
            assessment_result=assessment_result, attempt=attempt)
    except IndividualFeedback.DoesNotExist:
        feedback = IndividualFeedback.objects.create(
            assessment_result=assessment_result,
            attempt=attempt,
            marking_date=datetime.date.today(),
        )
        if assessment.co_marking:
            for staff in module.teachers.all():
                feedback.markers.add(staff)
        else:
            feedback.markers.add(request.user.staff)
    mark = assessment_result.get_one_mark(attempt)
    if attempt == 'first':
        marksheet_type = assessment.marksheet_type
    else:
        marksheet_type = assessment.resit_marksheet_type
    IndividualFeedbackForm = get_individual_feedback_form(marksheet_type)
    if request.method == 'POST':
        form = IndividualFeedbackForm(instance=feedback, data=request.POST)
        if form.is_valid():
            form.save()
            mark = form.cleaned_data['mark']
            assessment_result.set_one_mark(attempt, int(mark))
            if form.cleaned_data['mark']:
                if form.cleaned_data['submission_date']:
                    if form.cleaned_data['marking_date']:
                        feedback.completed = True
                        feedback.save()
            return redirect(module.get_absolute_url())
    else:
        form = IndividualFeedbackForm(
            instance=feedback,
            initial={'mark': mark},
        )

    return render(
        request,
        'individual_feedback.html',
        {
            'student': student,
            'form': form,
            'module': module,
            'assessment': assessment,
            'marksheet_type': marksheet_type,
        }
    )


def group_feedback(
        request, code, year, assessment_slug, student_id, attempt='first'):

    module = Module.objects.get(code=code, year=year)
    assessment = Assessment.objects.get(module=module, slug=assessment_slug)
    this_student = Student.objects.get(student_id=student_id)
    jump_to = '#' + this_student.student_id
    performance = Performance.objects.get(module=module, student=this_student)
    assessment_result = AssessmentResult.objects.get(
        assessment=assessment, part_of=performance)
    group_number = assessment_result.assessment_group
    try:
        group_feedback = GroupFeedback.objects.get(
            assessment=assessment,
            group_number=group_number,
            attempt=attempt,
        )
    except GroupFeedback.DoesNotExist:
        group_feedback = GroupFeedback.objects.create(
            assessment=assessment,
            group_number=group_number,
            attempt=attempt,
            marking_date=datetime.date.today(),
        )
        if assessment.co_marking:
            for staff in module.teachers.all():
                group_feedback.markers.add(staff)
        else:
            group_feedback.markers.add(request.user.staff)
    results_in_group = AssessmentResult.objects.filter(
        assessment=assessment,
        assessment_group=group_number
    )
    students_in_group = []
    original_marks = {}
    feedback_dict = {}
    for assessment_result in results_in_group:
        student = assessment_result.part_of.first().student
        students_in_group.append(student)
        try:
            feedback = IndividualFeedback.objects.get(
                assessment_result=assessment_result,
                attempt=attempt
            )
        except IndividualFeedback.DoesNotExist:
            feedback = IndividualFeedback.objects.create(
                assessment_result=assessment_result,
                attempt=attempt
            )
        feedback_dict[student.student_id] = feedback
        original_marks[student.student_id] = assessment_result.get_one_mark(
            attempt)
    if attempt == 'first':
        marksheet_type = assessment.marksheet_type
    else:
        marksheet_type = assessment.resit_marksheet_type
    IndividualFeedbackForm = get_individual_feedback_form_for_group(
        marksheet_type)
    GroupFeedbackForm = get_group_feedback_form(marksheet_type)

    if request.method == 'POST':
        group_form = GroupFeedbackForm(
            instance=group_feedback,
            data=request.POST,
            prefix='group'
        )
        student_forms = {}
        for student in students_in_group:
            student_form = IndividualFeedbackForm(
                instance=feedback_dict[student.student_id],
                data=request.POST,
                prefix=student.student_id
            )
            student_forms[student] = student_form
        if group_form.is_valid():
            valid = True
            for student in students_in_group:
                if not student_forms[student].is_valid():
                    valid = False
            if valid:
                group_form.save()
                data = group_form.cleaned_data
                group_mark = int(data['group_mark'])
                marksheet_type = CATEGORIES[assessment.marksheet_type]
                split = marksheet_type['split']
                group_weighting = int(split[0])
                individual_weighting = int(split[1])
                together = group_weighting + individual_weighting
                group_part = group_mark * group_weighting
                group_feedback = GroupFeedback.objects.get(
                    assessment=assessment,
                    group_number=group_number,
                    attempt=attempt
                )
                group_feedback.completed = True
                group_feedback.save()
                for student in students_in_group:
                    student_forms[student].save()
                    data = student_forms[student].cleaned_data
                    individual_mark = int(data['individual_mark'])
                    performance = Performance.objects.get(
                        student=student,
                        module=module
                    )
                    assessment_result = AssessmentResult.objects.get(
                        assessment=assessment,
                        part_of=performance
                    )
                    individual_part = individual_mark * individual_weighting
                    mark_sum = group_part + individual_part
                    mark = int(round(mark_sum/together))
                    assessment_result.set_one_mark(attempt, mark)
                    feedback = IndividualFeedback.objects.get(
                        assessment_result=assessment_result,
                        attempt=attempt
                    )
                    feedback.completed = True
                    feedback.save()

                return redirect(module.get_absolute_url())

    else:
        group_form = GroupFeedbackForm(prefix='group', instance=group_feedback)
        student_forms = {}
        for student in students_in_group:
            student_form = IndividualFeedbackForm(
                instance=feedback_dict[student.student_id],
                prefix=student.student_id
            )
            student_forms[student] = student_form
        return render(
            request,
            'group_feedback.html',
            {
                'assessment': assessment,
                'group_form': group_form,
                'student_forms': student_forms,
                'jump_to': jump_to,
                'original_marks': original_marks,
                'group_number': group_number,
            }
        )

# Functions for Reportlab stuff


def logo():
    """Returns the university logo, unless it is not available"""
    styles = getSampleStyleSheet()
    url = "https://cccu.tobiaskliem.de/static/images/cccu.jpg"
    try:
        image = Image(url, 2.45*inch, 1*inch)
    except IOError:
        image = Paragraph(
            "Canterbury Christ Church University", styles['Heading1'])
    return image


def formatted_date(raw_date):
    """Returns a proper date string

    This returns a string of the date in British Format.
    If the date field was left blank, an empty string is returned.
    """
    if raw_date is None:
        result = ''
    else:
        result = (
            str(raw_date.day) + '/' + str(raw_date.month) + '/' +
            str(raw_date.year)
        )
    return result


def bold(string):
    """Adds <b> tags around a string"""
    bold_string = '<b>' + string + '</b>'
    return bold_string


def heading(string, headingstyle='Heading2'):
    """Returns a proper paragraph for the header line"""
    styles = getSampleStyleSheet()
    tmp = '<para alignment = "center">' + string + '</para>'
    result = Paragraph(tmp, styles[headingstyle])
    return result


def paragraph(string):
    """Returns a paragraph with normal style"""
    styles = getSampleStyleSheet()
    return Paragraph(string, styles['Normal'])


def bold_paragraph(string):
    """Returns a paragraph with bold formatting"""
    styles = getSampleStyleSheet()
    tmp = bold(string)
    return Paragraph(tmp, styles['Normal'])


def marker_string(markers):
    """Returns a string of all markers"""
    if len(markers) == 1:
        marker_str = markers[0].name()
    else:
        marker_list = []
        for marker in markers:
            marker_list.append(marker.name())
        marker_str = ' / '.join(marker_list)
    return marker_str


# Individual Marksheets (for use by functions below)


def individual_marksheet(assessment, student, attempt):
    """Marksheet for the standard Individual Marksheets"""
    styles = getSampleStyleSheet()
    elements = []
    module = assessment.module
    performance = Performance.objects.get(student=student, module=module)
    assessment_result = AssessmentResult.objects.get(
        assessment=assessment, part_of=performance)
    feedback = IndividualFeedback.objects.get(
        assessment_result=assessment_result, attempt=attempt)
    assessment_title = bold(assessment.title)
    if attempt == 'first':
        mark = str(assessment_result.mark)
    elif attempt == 'resit':
        mark = str(assessment_result.resit_mark)
    elif attempt == 'second_resit':
        mark = str(assessment_result.second_resit_mark)
    elif attempt == 'qld_resit':
        mark = str(assessment_result.qld_resit)
    elements.append(logo())
    elements.append(Spacer(1, 5))
    title = heading('Law Undergraduate Assessment Sheet')
    elements.append(title)
    elements.append(Spacer(1, 5))
    last_name = [
        paragraph('Student family name'),
        Spacer(1, 3),
        bold_paragraph(student.last_name)
    ]
    first_name = [
        paragraph('First name'),
        Spacer(1, 3),
        bold_paragraph(student.first_name)
    ]
    module_title = [
        paragraph('Module Title'),
        Spacer(1, 3),
        bold_paragraph(module.title)
    ]
    module_code = [
        paragraph('Module Code'),
        Spacer(1, 3),
        bold_paragraph(module.code)
    ]
    tmp = formatted_date(feedback.submission_date)
    submission_date = [
        paragraph('Submission Date'),
        Spacer(1, 3),
        bold_paragraph(tmp)
    ]
    assessment_title = [
        paragraph('Assessment Title'),
        Spacer(1, 3),
        bold_paragraph(assessment.title)
    ]
    if assessment.max_word_count:
        tmp = (
            str(assessment.max_word_count) +
            ' Words max.'
        )
    else:
        tmp = None
    if tmp:
        word_count = [
            paragraph('Word Count'),
            Spacer(1, 3),
            bold_paragraph(tmp)
        ]
    else:
        word_count = ''
    if attempt == 'first':
        marksheet_type = CATEGORIES[assessment.marksheet_type]
    else:
        marksheet_type = CATEGORIES[assessment.marksheet_type_resit]
    if assessment.marksheet_type == 'MEDIATION_ROLE_PLAY':  # Other marksheets
        data = [
            [last_name, first_name],
            [module_title, module_code],
            [assessment_title, submission_date],
        ]
        t1 = Table(data)
        t1.setStyle(
            TableStyle(
                [
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
                ]
            )
        )
        elements.append(t1)
        elements.append(Spacer(1, 4))
        data = [
            [
                paragraph('Mode of Assessment'),
                paragraph('Assessment Criteria'),
                paragraph('Mark')
            ]
        ]
        for x in range(1, 4):
            category = 'i-' + str(x)
            row = [paragraph(marksheet_type[category])]
            helptext = category + '-helptext'
            row.append(paragraph(marksheet_type[helptext]))
            row.append(str(feedback.category_mark(x, free=True)))
            data.append(row)
        t = Table(data, colWidths=[1*inch, 4.4*inch, .7*inch])
        t.setStyle(
            TableStyle(
                [
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                    ('ALIGN', (-1, 1), (-1, -1), 'RIGHT'),
                ]
            )
        )

    else:  # The standard marksheets following the standard template
        criteria = paragraph('Criteria')
        categorylist = [criteria]
        number = marksheet_type['number_of_categories']
        for x in range(1, number+1):
            tmp = 'i-' + str(x)
            categorylist.append(paragraph(marksheet_type[tmp]))
        if number < 4:
            data = [
                [last_name, '', first_name],
                [module_title, '', module_code, submission_date],
                [assessment_title, '', word_count, ''],
                categorylist
            ]
        elif number == 4:
            data = [
                [last_name, '', first_name, ''],
                [module_title, '', module_code, submission_date, ''],
                [assessment_title, '', word_count, '', ''],
                categorylist
            ]
        row = ['80 +']
        for category in range(1, number+1):
            if feedback.category_mark(category) == 80:
                row.append('X')
            else:
                row.append(' ')
        data.append(row)
        row = ['70 - 79']
        for category in range(1, number+1):
            if feedback.category_mark(category) == 79:
                row.append('X')
            else:
                row.append(' ')
        data.append(row)
        row = ['60 - 69']
        for category in range(1, number+1):
            if feedback.category_mark(category) == 69:
                row.append('X')
            else:
                row.append(' ')
        data.append(row)
        row = ['50 - 59']
        for category in range(1, number+1):
            if feedback.category_mark(category) == 59:
                row.append('X')
            else:
                row.append(' ')
        data.append(row)
        row = ['40 - 49']
        for category in range(1, number+1):
            if feedback.category_mark(category) == 49:
                row.append('X')
            else:
                row.append(' ')
        data.append(row)
        row = ['30 - 39']
        for category in range(1, number+1):
            if feedback.category_mark(category) == 39:
                row.append('X')
            else:
                row.append(' ')
        data.append(row)
        row = ['Under 30']
        for category in range(1, number+1):
            if feedback.category_mark(category) == 29:
                row.append('X')
            else:
                row.append(' ')
        data.append(row)
        t = Table(data)
        if word_count:
            wordcount_row_1 = ('SPAN', (0, 2), (1, 2))
            wordcount_row_2 = ('SPAN', (2, 2), (-1, 2))
        else:
            wordcount_row_1 = ('SPAN', (0, 2), (-1, 2))
            wordcount_row_2 = ('SPAN', (0, 2), (-1, 2))
        t.setStyle(
            TableStyle(
                [
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('SPAN', (0, 0), (1, 0)),
                    ('SPAN', (2, 0), (-1, 0)),
                    ('SPAN', (0, 1), (1, 1)),
                    ('SPAN', (3, 1), (-1, 1)),
                    wordcount_row_1,
                    wordcount_row_2,
                    ('BACKGROUND', (0, 3), (-1, 3), colors.lightgrey),
                    ('BACKGROUND', (0, 4), (0, -1), colors.lightgrey),
                    ('ALIGN', (1, 4), (-1, -1), 'CENTER'),
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
                ]
            )
        )
    elements.append(t)
    elements.append(Spacer(1, 4))
    comments = [
        bold_paragraph('General Comments'),
        Spacer(1, 4)
    ]
    feedbacklist = feedback.comments.split('\n')
    for line in feedbacklist:
        if line != "":
            p = paragraph(line)
            comments.append(p)
            comments.append(Spacer(1, 4))
    for comment in comments:
        elements.append(comment)
    markers = feedback.markers.all()
    marker_str = marker_string(markers)
    marking_date = formatted_date(feedback.marking_date)
    marked_by = [
        [paragraph('Marked by'), bold_paragraph(marker_str)],
        [paragraph('Date'), bold_paragraph(marking_date)]
    ]
    marked_by_table = Table(marked_by)
    mark = [
        [paragraph('Mark'), Paragraph(mark, styles['Heading1'])],
        ['', '']
    ]
    mark_table = Table(mark)
    mark_table.setStyle(TableStyle([('SPAN', (1, 0), (1, 1))]))
    last_data = [[marked_by_table, '', '', mark_table, '']]
    last_table = Table(last_data)
    last_table.setStyle(
        TableStyle(
            [
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ('SPAN', (0, 0), (2, 0)),
                ('SPAN', (3, -1), (-1, -1))
            ]
        )
    )
    elements.append(last_table)
    return elements


def group_presentation_marksheet(assessment, student, attempt):
    """Marksheet for the standard Group Presentation Marksheets"""
    styles = getSampleStyleSheet()
    elements = []
    module = assessment.module
    performance = Performance.objects.get(student=student, module=module)
    assessment_result = AssessmentResult.objects.get(
        assessment=assessment, part_of=performance)
    feedback = IndividualFeedback.objects.get(
        assessment_result=assessment_result,
        attempt=attempt
    )
    group_feedback = GroupFeedback.objects.get(
        assessment=assessment,
        group_number=assessment_result.assessment_group,
        attempt=attempt
    )
    assessment_title = bold(assessment.title)
    if attempt == 'first':
        marksheet_type = CATEGORIES[assessment.marksheet_type]
    else:
        marksheet_type = CATEGORIES[assessment.marksheet_type_resit]
    if attempt == 'first':
        mark = str(assessment_result.mark)
    elif attempt == 'resit':
        mark = str(assessment_result.resit_mark)
    elif attempt == 'second_resit':
        mark = str(assessment_result.second_resit_mark)
    elif attempt == 'qld_resit':
        mark = str(assessment_result.qld_resit)
    elements.append(logo())
    elements.append(Spacer(1, 5))
    title = heading('Law Undergraduate Assessment Sheet')
    elements.append(title)
    elements.append(Spacer(1, 5))
    last_name = [
        paragraph('Student family name'),
        Spacer(1, 3),
        bold_paragraph(student.last_name)
    ]
    first_name = [
        paragraph('First name'),
        Spacer(1, 3),
        bold_paragraph(student.first_name)
    ]
    module_title = [
        paragraph('Module Title'),
        Spacer(1, 3),
        bold_paragraph(module.title)
    ]
    module_code = [
        paragraph('Module Code'),
        Spacer(1, 3),
        bold_paragraph(module.code)
    ]
    tmp = formatted_date(group_feedback.submission_date)
    submission_date = [
        paragraph('Date'),
        Spacer(1, 3),
        bold_paragraph(tmp)
    ]
    assessment_title = [
        paragraph('Assessment Title'),
        Spacer(1, 3),
        bold_paragraph(assessment.title)
    ]
    group_no = [
        paragraph('Group Number'),
        Spacer(1, 3),
        bold_paragraph(str(assessment_result.assessment_group))
    ]
    criteria = paragraph('Criteria')
    categorylist = [criteria]
    i_number = marksheet_type['number_of_individual_categories']
    g_number = marksheet_type['number_of_group_categories']
    number = i_number + g_number
    for x in range(1, i_number+1):
        tmp = 'i-' + str(x)
        categorylist.append(paragraph(marksheet_type[tmp]))
    for x in range(1, g_number+1):
        tmp = 'g-' + str(x)
        categorylist.append(paragraph(marksheet_type[tmp]))
    data = [
        [last_name, '', first_name, '', group_no, ''],
        [module_title, '', assessment_title, '', module_code, submission_date],
        [
            '',
            bold_paragraph('Individual Component'),
            '',
            '',
            bold_paragraph('Group Component'),
            ''
        ],
        categorylist
    ]
    row = ['80 +']
    for category in range(1, i_number+1):
        if feedback.category_mark(category) == 80:
            row.append('X')
        else:
            row.append(' ')
    for category in range(1, g_number+1):
        if group_feedback.category_mark(category) == 80:
            row.append('X')
        else:
            row.append(' ')
    data.append(row)
    row = ['70 - 79']
    for category in range(1, i_number+1):
        if feedback.category_mark(category) == 79:
            row.append('X')
        else:
            row.append(' ')
    for category in range(1, g_number+1):
        if group_feedback.category_mark(category) == 79:
            row.append('X')
        else:
            row.append(' ')
    data.append(row)
    row = ['60 - 69']
    for category in range(1, i_number+1):
        if feedback.category_mark(category) == 69:
            row.append('X')
        else:
            row.append(' ')
    for category in range(1, g_number+1):
        if group_feedback.category_mark(category) == 69:
            row.append('X')
        else:
            row.append(' ')
    data.append(row)
    row = ['50 - 59']
    for category in range(1, i_number+1):
        if feedback.category_mark(category) == 59:
            row.append('X')
        else:
            row.append(' ')
    for category in range(1, g_number+1):
        if group_feedback.category_mark(category) == 59:
            row.append('X')
        else:
            row.append(' ')
    data.append(row)
    row = ['40 - 49']
    for category in range(1, i_number+1):
        if feedback.category_mark(category) == 49:
            row.append('X')
        else:
            row.append(' ')
    for category in range(1, g_number+1):
        if group_feedback.category_mark(category) == 49:
            row.append('X')
        else:
            row.append(' ')
    data.append(row)
    row = ['30 - 39']
    for category in range(1, i_number+1):
        if feedback.category_mark(category) == 39:
            row.append('X')
        else:
            row.append(' ')
    for category in range(1, g_number+1):
        if group_feedback.category_mark(category) == 39:
            row.append('X')
        else:
            row.append(' ')
    data.append(row)
    row = ['Under 30']
    for category in range(1, i_number+1):
        if feedback.category_mark(category) == 29:
            row.append('X')
        else:
            row.append(' ')
    for category in range(1, g_number+1):
        if group_feedback.category_mark(category) == 29:
            row.append('X')
        else:
            row.append(' ')
    data.append(row)
    t = Table(data)
    t.setStyle(
        TableStyle(
            [
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('SPAN', (0, 0), (1, 0)),
                ('SPAN', (2, 0), (3, 0)),
                ('SPAN', (4, 0), (5, 0)),
                ('SPAN', (0, 1), (1, 1)),
                ('SPAN', (2, 1), (3, 1)),
                ('SPAN', (1, 2), (3, 2)),
                ('SPAN', (4, 2), (-1, 2)),
                ('BACKGROUND', (0, 2), (-1, 2), colors.lightgrey),
                ('BACKGROUND', (0, 3), (-1, 3), colors.lightgrey),
                ('BACKGROUND', (0, 4), (0, -1), colors.lightgrey),
                ('ALIGN', (1, 4), (-1, -1), 'CENTER'),
                ('BOX', (0, 2), (0, -1), 1, colors.black),
                ('BOX', (0, 0), (-1, 1), 1, colors.black),
                ('BOX', (4, 2), (-1, -1), 1, colors.black),
                ('BOX', (0, 2), (0, -1), 1, colors.black),
                ('BOX', (1, 2), (3, -1), 1, colors.black),
            ]
        )
    )
    elements.append(t)
    elements.append(Spacer(1, 4))
    group_comments = [
        bold_paragraph('Comments on the Group Performance'),
        Spacer(1, 4)
    ]
    feedbacklist = group_feedback.comments.split('\n')
    for line in feedbacklist:
        if line != "":
            p = paragraph(line)
            group_comments.append(p)
            group_comments.append(Spacer(1, 4))
    for comment in group_comments:
        elements.append(comment)
    elements.append(Spacer(1, 4))
    comments = [
        bold_paragraph('Comments on the Individual Performance'),
        Spacer(1, 4)
    ]
    feedbacklist = feedback.comments.split('\n')
    for line in feedbacklist:
        if line != "":
            p = paragraph(line)
            comments.append(p)
            comments.append(Spacer(1, 4))
    for comment in comments:
        elements.append(comment)
    markers = group_feedback.markers.all()
    marker_str = marker_string(markers)
    marking_date = formatted_date(group_feedback.marking_date)
    marked_by = [
        [paragraph('Marked by'), bold_paragraph(marker_str)],
        [paragraph('Date'), bold_paragraph(marking_date)]
    ]
    marked_by_table = Table(marked_by)
    mark = [
        [paragraph('Mark'), Paragraph(mark, styles['Heading1'])],
        ['', '']
    ]
    mark_table = Table(mark)
    mark_table.setStyle(TableStyle([('SPAN', (1, 0), (1, 1))]))
    last_data = [[marked_by_table, '', '', mark_table, '']]
    last_table = Table(last_data)
    last_table.setStyle(
        TableStyle(
            [
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ('SPAN', (0, 0), (2, 0)),
                ('SPAN', (3, -1), (-1, -1))
            ]
        )
    )
    elements.append(last_table)
    return elements


# Export functions called from the website

def export_feedback(
        request, code, year, assessment_slug, student_id, attempt='first'):
    """Will export either one or multiple feedback sheets.

    This needs to be given the student id or the string 'all' if
    you want all marksheets for the assessment. It will only work if
    the person requesting is a teacher, an admin or the student the
    marksheet is about.
    """
    module = Module.objects.get(code=code, year=year)
    assessment = Assessment.objects.get(module=module, slug=assessment_slug)
    if attempt == 'first':
        assessment_type = assessment.marksheet_type
    else:
        assessment_type = assessment.marksheet_type_resit
    if student_id == 'all':
        if is_staff(request.user):
            response = HttpResponse(content_type='application/pdf')
            filename_string = (
                'attachment; filename=' +
                assessment.filename() +
                '_-_all_marksheets.pdf'
            )
            all_students = module.students.all()
            documentlist = []
            students = []  # Only the students where feedback has been entered
            for student in all_students:
                performance = Performance.objects.get(
                    student=student, module=module)
                try:
                    result = AssessmentResult.objects.get(
                        part_of=performance, assessment=assessment)
                    try:
                        feedback = IndividualFeedback.objects.get(
                            assessment_result=result, attempt=attempt)
                        if feedback.completed:
                            students.append(student)
                    except IndividualFeedback.DoesNotExist:
                        pass
                except AssessmentResult.DoesNotExist:
                    pass
            for student in students:
                if assessment.group_assessment:
                    elements = group_presentation_marksheet(
                        assessment, student, attempt)
                    pass
                else:
                    elements = individual_marksheet(
                        assessment, student, attempt)
                for element in elements:
                    documentlist.append(element)
                documentlist.append(PageBreak())
            response['Content-Disposition'] = filename_string
            document = SimpleDocTemplate(response)
            uni_name = Setting.objects.get(name="uni_name").value
            document.setAuthor = uni_name
            document.setTitle = 'Marksheet'
            document.build(documentlist)
            return response
        else:
            return HttpResponseForbidden()
    else:
        student = Student.objects.get(student_id=student_id)
        own_marksheet = False  # Just for the filename
        allowed = False
        if is_staff(request.user):
            allowed = True
        elif is_student(request.user):
            if student.user == request.user:
                own_marksheet = True
                allowed = True
        if allowed:
            response = HttpResponse(content_type='application/pdf')
            filename_string = 'attachment; filename=' + assessment.filename()
            if not own_marksheet:
                ln = student.last_name.replace(' ', '_')
                fn = student.first_name.replace(' ', '_')
                filename_string += ln + '_' + fn
            filename_string += '.pdf'
            response['Content-Disposition'] = filename_string
            document = SimpleDocTemplate(response)
            uni_name = Setting.objects.get(name="uni_name").value
            document.setAuthor = uni_name
            if assessment.group_assessment:
                elements = group_presentation_marksheet(
                    assessment, student, attempt)
                pass
            else:
                elements = individual_marksheet(
                    assessment, student, attempt)
            document.build(elements)
            return response
        else:
            return HttpResponseForbidden()
