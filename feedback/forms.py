from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Fieldset, HTML, Div
from crispy_forms.bootstrap import TabHolder, Tab, FormActions
from main.models import *
from feedback.models import *
from feedback.categories import CATEGORIES

def get_individual_feedback_form(marksheet_type):

    if marksheet_type == 'ESSAY':

        class IndividualFeedbackForm(forms.ModelForm):

            mark = forms.IntegerField()
            helper = FormHelper()
            helper.layout = Layout(
                'marker',
                'marking_date',
                'submission_date',
                'category_mark_1',
                # Tooltip: HTML(),
                'category_mark_2',
                'category_mark_3',
                'category_mark_4',
                'comments',
                'mark'
            )

            def __init__(self, *args, **kwargs):
                super(IndividualFeedbackForm, self).__init__(*args, **kwargs)
                self.fields['category_mark_1'].label = (
                    CATEGORIES['ESSAY']['i-1'])
                self.fields['category_mark_2'].label = (
                    CATEGORIES['ESSAY']['i-2'])
                self.fields['category_mark_3'].label = (
                    CATEGORIES['ESSAY']['i-3'])
                self.fields['category_mark_4'].label = (
                    CATEGORIES['ESSAY']['i-4'])

            def save(self, commit=True):
                # save mark
                super(IndividualFeedbackForm, self).save(commit=commit)

            class Meta:
                model = IndividualFeedback
                fields = [
                    'marker',
                    'marking_date',
                    'submission_date',
                    'comments',
                    'category_mark_1',
                    'category_mark_2',
                    'category_mark_3',
                    'category_mark_4',
                ]
    return IndividualFeedbackForm
