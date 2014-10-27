from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Fieldset, HTML, Div
from crispy_forms.bootstrap import TabHolder, Tab, FormActions, PrependedText
from main.models import *
from feedback.models import *
from feedback.categories import CATEGORIES

def get_individual_helptext_html(marksheet_type, number):
    numberstr = 'i-' + str(number) + '-helptext'
    category = CATEGORIES[marksheet_type]
    helptext = category[numberstr]
    html = (
        '<span class="glyphicon glyphicon-question-sign" data-toggle=' +
        '"tooltip" data-placement="bottom" data-html="true" title="' +
        helptext +
        '"></span>'
    )
    return html


def get_individual_feedback_form(marksheet_type):

    if marksheet_type == 'ESSAY':

        class IndividualFeedbackForm(forms.ModelForm):
            mark = forms.IntegerField(
                validators=[MaxValueValidator(100), MinValueValidator(0)]
            )
            helper = FormHelper()
            helper.layout = Layout(
                Field('markers', css_class='chosen-select'),
                Field('marking_date', css_class='datepicker'),
                Field('submission_date', css_class='datepicker'),
                PrependedText(
                    'category_mark_1',
                    get_individual_helptext_html(marksheet_type, 1)
                ),
                PrependedText(
                    'category_mark_2',
                    get_individual_helptext_html(marksheet_type, 2)
                ),
                PrependedText(
                    'category_mark_3',
                    get_individual_helptext_html(marksheet_type, 3)
                ),
                PrependedText(
                    'category_mark_4',
                    get_individual_helptext_html(marksheet_type, 4)
                ),
                'comments',
                'mark',
                FormActions(
                    Submit(
                        'save', 'Save', css_class="btn btn-primary")
                )
            )
            helper.form_class = "form-horizontal"
            helper.label_class = "col-lg-4 col-md-2 col-sm-2"
            helper.field_class = "col-lg-6 col-md-8 col-sm-10"

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

            class Meta:
                model = IndividualFeedback
                fields = [
                    'markers',
                    'marking_date',
                    'submission_date',
                    'comments',
                    'category_mark_1',
                    'category_mark_2',
                    'category_mark_3',
                    'category_mark_4',
                ]
    return IndividualFeedbackForm
