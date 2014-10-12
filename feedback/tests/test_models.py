from .base import *
from main.models import *
from feedback.models import *

class IndividualFeedbackTest(TeacherUnitTest):
    """Tests around the Individual Feedback Model"""

    def test_feedback_can_be_saved(self):
        assessment = create_assessment()
        assessment_out = Assessment.objects.first()
        self.assertEqual(assessment, assessment_out)
