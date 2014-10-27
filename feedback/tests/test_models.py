from .base import *
from main.models import *
from feedback.models import *

class IndividualFeedbackTest(TeacherUnitTest):
    """Tests around the Individual Feedback Model"""

    def test_feedback_can_be_saved(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student = stuff[1]
        assessment = Assessment.objects.create(
            module=module,
            title='Dissertation',
            value=100
        )
        feedback = IndividualFeedback()
        assessment_out = Assessment.objects.first()
        self.assertEqual(assessment, assessment_out)
