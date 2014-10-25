from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Fieldset, HTML, Div
from crispy_forms.bootstrap import TabHolder, Tab, FormActions
from main.models import *
from feedback.models import *
from feedback.categories import CATEGORIES

class IndividualFeedbackForm(forms.ModelForm):

    mark = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        marksheet_type = kwargs.pop('marksheet_type')
        super(IndividualFeedbackForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        if marksheet_type == 'ESSAY':
            print('essay')
            self.helper.layout = Layout(
                'marker',
                'marking_date',
                'submission_date',
                Field('category_mark_1', label=CATEGORIES['ESSAY']['i-1']),
                Field('category_mark_2', label=CATEGORIES['ESSAY']['i-2']),
                Field('category_mark_3', label=CATEGORIES['ESSAY']['i-3']),
                Field('category_mark_4', label=CATEGORIES['ESSAY']['i-4']),
                'comments',
                'mark'
            )


    def save(self, commit=True):
        # save mark
        super(IndividualFeedbackForm, self).save(commit=commit)

    class Meta:
        model = IndividualFeedback
        try:
            if marksheet_type == 'ESSAY':
                print('Jaha')
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
        except NameError:
            fields = [
                'marker',
                'marking_date',
                'submission_date',
                'comments',
                'category_mark_1',
                'category_mark_2',
                'category_mark_3',
                'category_mark_4',
                'category_mark_5',
                'category_mark_6',
                'category_mark_7',
                'category_mark_8',
            ]
