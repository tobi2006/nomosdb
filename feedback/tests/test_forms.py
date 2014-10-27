from .base import *
from feedback.forms import *

class IndividualFeedbackFormTests(TeacherUnitTest):
    """Testing the Individual Feedback Form"""

    def test_form_is_generated_correctly_for_essay(self):
        IndividualFeedbackForm = get_individual_feedback_form('ESSAY')
        form = IndividualFeedbackForm()
        self.assertIn('id="id_markers"', form.as_p())
        self.assertIn('id="id_marking_date"', form.as_p())
        self.assertIn('id="id_submission_date"', form.as_p())
        self.assertIn('id="id_category_mark_1"', form.as_p())
        self.assertIn('id="id_category_mark_2"', form.as_p())
        self.assertIn('id="id_category_mark_3"', form.as_p())
        self.assertIn('id="id_category_mark_4"', form.as_p())
        self.assertNotIn('id="id_category_mark_5"', form.as_p())
        self.assertNotIn('id="id_category_mark_6"', form.as_p())
        self.assertNotIn('id="id_category_mark_7"', form.as_p())
        self.assertNotIn('id="id_category_mark_8"', form.as_p())
        self.assertIn('id="id_comments"', form.as_p())
        self.assertIn('id="id_mark"', form.as_p())

