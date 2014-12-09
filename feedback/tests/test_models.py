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
        student_1 = stuff[1]
        student_2 = stuff[2]
        feedback_in = GroupFeedback(
            group_no=1,
            attempt='first'
        )
        comment = 'Generally a good presentation, but too many carrots'
        feedback_in.set_individual_part(1, student_1.student_id, 40)
        feedback_in.set_individual_part(
            'comments',
            student_1.student_id,
            comment
        )
        feedback_in.set_individual_part(1, student_2.student_id, 50)
        feedback_out = GroupFeedback.objects.first()
        self.assertEqual(
            feedback_out.get_individual_part(1, student_1.student_id),
            40
        )
        self.assertEqual(
            feedback_out.get_individual_part(1, student_2.student_id),
            50
        )
        self.assertEqual(
            feedback_out.get_individual_part('comments', student_1.student_id),
            comment
        )

    def test_multiple_individual_categories_can_be_saved(self):
        stuff = set_up_stuff()
        module = stuff[0]
        student_1 = stuff[1]
        student_2 = stuff[2]
        feedback_in = GroupFeedback(
            group_no=1,
            attempt='first'
        )
        marks = {student_1.student_id: 45, student_2.student_id: 55}
        comments = {student_1.student_id: 'aaa', student_2.student_id: 'bbb'}
        feedback_in.set_multiple_individual_parts(1, marks)
        feedback_in.set_multiple_individual_parts('comments', comments)
        feedback_out = GroupFeedback.objects.first()
        self.assertEqual(
            feedback_out.get_individual_part(1, student_1.student_id),
            45
        )
        self.assertEqual(
            feedback_out.get_individual_part(1, student_2.student_id),
            55
        )
        self.assertEqual(
            feedback_out.get_individual_part('comments', student_1.student_id),
            'aaa'
        )
        self.assertEqual(
            feedback_out.get_individual_part('comments', student_2.student_id),
            'bbb'
        )
