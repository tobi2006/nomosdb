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


class GroupFeedbackTest(TeacherUnitTest):
    """Tests around the group feedback model"""

    def test_individual_categories_can_be_saved_and_retrieved(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student1 = stuff[1]
        student2 = stuff[2]
        assessment = Assessment.objects.create(
            module=module,
            title='Group Presentation',
            value=100
        )
        feedback_in = GroupFeedback(
            assessment=assessment,
            group_no=1,
            attempt='first'
        )
        feedback_in.set_individual_mark(1, student_1.student_id, 40)
        feedback_in.set_individual_mark(1, student_2.student_id, 50)
        feedback_out.GroupFeedback.objects.first()
        self.assertEqual(
            feedback_out.get_individual_mark(1, student_1.student_id),
            40
        )
        self.assertEqual(
            feedback_out.get_individual_mark(1, student_2.student_id),
            50
        )
