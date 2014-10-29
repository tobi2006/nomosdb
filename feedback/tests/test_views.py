from .base import *
from main.models import *
from feedback.models import *
from feedback.views import *
from main.views import *
import datetime


class ModuleViewTests(TeacherUnitTest):
    """Tests about the feedback integration into Module View"""

    def test_pencil_symbol_appears_for_assessments_with_marksheet(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student = stuff[1]
        assessment1 = Assessment.objects.create(
            module=module,
            title='Essay',
            value=20,
            marksheet_type='ESSAY'
        )
        assessment2 = Assessment.objects.create(
            module=module,
            title='Presentation',
            value=30,
            marksheet_type='PRESENTATION'
        )
        assessment_3 = Assessment.objects.create(
            module=module,
            title='Strange Assessment',
            value=20,
            marksheet_type='there_is_none_yet'
        )
        assessment_4 = Assessment.objects.create(
            module=module,
            title='Exam',
            value=30
        )
        request = self.factory.get(module.get_absolute_url())
        request.user = self.user
        response = module_view(request, module.code, module.year)
        linktext = (
            '<a href="' +
            assessment1.get_blank_feedback_url() +
            student.student_id +
            '/first/"><span class="glyphicon glyphicon-pencil"></span></a>'
        )
        should_not_be_in = (
            '<a href="' +
            assessment_4.get_blank_feedback_url() +
            student.student_id +
            '/first/"><span class="glyphicon glyphicon-pencil"></span></a>'
        )
        self.assertContains(
            response,
            linktext,
            html=True
        )
        self.assertNotContains(
            response,
            should_not_be_in,
            html=True
        )


class IndividualFeedbackTest(TeacherUnitTest):
    """Tests the Individual Feedback View"""

    def test_individual_feedback_form_uses_correct_template(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student = stuff[1]
        assessment = Assessment.objects.create(
            module=module,
            title='Essay',
            value=100,
            marksheet_type='ESSAY'
        )
        url = (
            assessment.get_blank_feedback_url() +
            student.student_id +
            '/first/'
        )
        request = self.factory.get(url)
        request.user = self.user
        response = individual_feedback(
            request,
            module.code,
            module.year,
            assessment.slug,
            student.student_id,
            'first'
        )
        self.assertTemplateUsed(response, 'individual_feedback.html')

    def test_form_view_shows_with_or_without_existing_feedback_object(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student = stuff[1]
        assessment = Assessment.objects.create(
            module=module,
            title='Essay',
            value=100,
            marksheet_type='ESSAY'
        )
        url = (
            assessment.get_blank_feedback_url() +
            student.student_id +
            '/first/'
        )
        request = self.factory.get(url)
        request.user = self.user
        response = individual_feedback(
            request,
            module.code,
            module.year,
            assessment.slug,
            student.student_id,
            'first'
        )
        self.assertEqual(response.status_code, 200)
        # Now, an individual feedback object should be created
        self.assertEqual(IndividualFeedback.objects.count(), 1)
        request = self.factory.get(url)
        request.user = self.user
        response = individual_feedback(
            request,
            module.code,
            module.year,
            assessment.slug,
            student.student_id,
            'first'
        )
        self.assertEqual(response.status_code, 200)

    def test_submitting_form_saves_feedback_and_mark(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student = stuff[1]
        assessment = Assessment.objects.create(
            module=module,
            title='Essay',
            value=100,
            marksheet_type='ESSAY'
        )
        url = (
            assessment.get_blank_feedback_url() +
            student.student_id +
            '/first/'
        )
        request = self.factory.post(
            url,
            data={
                'marking_date': '1/2/1900',
                'submission_date': '1/1/1900',
                'category_mark_1': 29,
                'category_mark_2': 39,
                'category_mark_3': 49,
                'category_mark_4': 59,
                'comments': 'Well done!',
                'mark': 76,
            }
        )
        request.user = self.user
        response = individual_feedback(
            request,
            module.code,
            module.year,
            assessment.slug,
            student.student_id,
            'first'
        )
        self.assertEqual(IndividualFeedback.objects.count(), 1)
        feedback = IndividualFeedback.objects.first()
        self.assertEqual(feedback.marking_date, datetime.date(1900, 2, 1))
        self.assertEqual(feedback.submission_date, datetime.date(1900, 1, 1))
        self.assertEqual(feedback.category_mark_1, 29)
        self.assertEqual(feedback.category_mark_2, 39)
        self.assertEqual(feedback.category_mark_3, 49)
        self.assertEqual(feedback.category_mark_4, 59)
        self.assertEqual(feedback.comments, 'Well done!')
        performance = Performance.objects.get(student=student, module=module)
        self.assertEqual(
            performance.get_assessment_result(assessment.slug, 'first'),
            76
        )
