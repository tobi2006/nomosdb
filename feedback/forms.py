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


def fieldname(marksheet_type, number):
    check = 'i-' + str(number) + '-free'
    category = CATEGORIES[marksheet_type]
    field_string = 'category_mark_' + str(number)
    if category[check]:
        field_string += '_free'
    return field_string


def get_individual_feedback_form(marksheet_type):

    feedback_type = CATEGORIES[marksheet_type]
    number = int(feedback_type['number_of_categories'])

    class IndividualFeedbackForm(forms.ModelForm):
        mark = forms.IntegerField(
            validators=[MaxValueValidator(100), MinValueValidator(0)]
        )
        helper = FormHelper()
        if number == 3:
            helper.layout = Layout(
                Field('markers', css_class='chosen-select'),
                Field('marking_date', css_class='datepicker'),
                Field('submission_date', css_class='datepicker'),
                PrependedText(
                    fieldname(marksheet_type, 1),
                    get_individual_helptext_html(marksheet_type, 1)
                ),
                HTML('<div id="error_1" class="has-error"></div>'),
                PrependedText(
                    fieldname(marksheet_type, 2),
                    get_individual_helptext_html(marksheet_type, 2)
                ),
                HTML('<div id="error_2" class="has-error"></div>'),
                PrependedText(
                    fieldname(marksheet_type, 3),
                    get_individual_helptext_html(marksheet_type, 3)
                ),
                HTML('<div id="error_3" class="has-error"></div>'),
                'comments',
                HTML('<div class="col-lg-4 col-md-2 col-sm-2"></div>' +
                        '<div class="col-lg-6 col-md-8 col-sm-10">' +
                        '<p id="penalty_suggestion" class="text-warning">' +
                        '</p></div>'
                ),
                'mark',
                FormActions(
                    Submit(
                        'save', 'Save', css_class="btn btn-primary")
                )
            )
        elif number == 4:
            helper.layout = Layout(
                Field('markers', css_class='chosen-select'),
                Field('marking_date', css_class='datepicker'),
                Field('submission_date', css_class='datepicker'),
                PrependedText(
                    fieldname(marksheet_type, 1),
                    get_individual_helptext_html(marksheet_type, 1)
                ),
                HTML('<div id="error_1" class="has-error"></div>'),
                PrependedText(
                    fieldname(marksheet_type, 2),
                    get_individual_helptext_html(marksheet_type, 2)
                ),
                HTML('<div id="error_2" class="has-error"></div>'),
                PrependedText(
                    fieldname(marksheet_type, 3),
                    get_individual_helptext_html(marksheet_type, 3)
                ),
                HTML('<div id="error_3" class="has-error"></div>'),
                PrependedText(
                    fieldname(marksheet_type, 4),
                    get_individual_helptext_html(marksheet_type, 4)
                ),
                HTML('<div id="error_4" class="has-error"></div>'),
                'comments',
                HTML('<div class="col-lg-4 col-md-2 col-sm-2"></div>' +
                        '<div class="col-lg-6 col-md-8 col-sm-10">' +
                        '<p id="penalty_suggestion" class="text-warning">' +
                        '</p></div>'
                ),
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
            for x in range(1, number + 1):
                field_name = fieldname(marksheet_type, x)
                labelname = 'i-' + str(x)
                self.fields[field_name].label = feedback_type[labelname]

        class Meta:
            model = IndividualFeedback
            fields = [
                'markers',
                'marking_date',
                'submission_date',
                'comments',
            ]
            for x in range(1, number + 1):
                fields.append(fieldname(marksheet_type, x))

    return IndividualFeedbackForm