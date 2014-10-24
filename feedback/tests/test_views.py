from .base import *
from main.models import *
from feedback.models import *
from feedback.views import *
from main.views import *

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
