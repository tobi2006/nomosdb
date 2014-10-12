from django.shortcuts import render
from datetime import datetime
from main.models import *
from feedback.models import *
from feedback.forms import *

# Create your views here.


def individual_feedback(
        request, code, year, assessment_slug, student_id, attempt='first'):
    """The form for all marksheets concerning just one student"""
    module = Module.objects.get(code=code, year=year)
    assessment = Assessment.objects.get(module=module, slug=assessment_slug)
    student = Student.objects.get(sudent_id=student_id)
    performance = Performance.objects.get(module=module, student=student)
    assessment_result = AssessmentResult.objects.get(
        assessment=assessment, part_of=performance)
    try:
        feedback = IndividualFeedback.objects.get(
            assessment_result=assessment_result, attempt=attempt)
    except IndividualFeedback.DoesNotExist:
        feedback = IndividualFeedback(
            assessment_result=assessment_result,
            attempt=attempt,
            marker=request.user.staff,
            marking_date= datetime.date.today(),
        )
    mark = asssessment_result.get_one_mark(attempt)
    if attempt == 'first':
        marksheet_type = assessment.marksheet_type
    else:
        marksheet_type = assessment.resit_marksheet_type
    form = IndividualFeedbackForm(
        initial = {'mark': mark},
        marksheet_type=marksheet_type
    )
