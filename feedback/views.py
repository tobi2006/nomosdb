from django.shortcuts import render, redirect
from datetime import datetime
from main.models import *
from feedback.models import *
from feedback.forms import *

# Create your views here.


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
            marking_date= datetime.date.today(),
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
        }
    )
