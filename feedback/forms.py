from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Fieldset, HTML, Div
from crispy_forms.bootstrap import TabHolder, Tab, FormActions, PrependedText
from main.models import *
from feedback.models import *
from feedback.categories import CATEGORIES

def get_helptext_html(marksheet_type, number, group=False):
    if group:
        numberstr = 'g-' + str(number) + '-helptext'
    else:
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


def fieldname(marksheet_type, number, group=False):
    if group:
        check = 'g-' + str(number) + '-free'
    else:
        check = 'i-' + str(number) + '-free'
    category = CATEGORIES[marksheet_type]
    field_string = 'category_mark_' + str(number)
    if category[check]:
        field_string += '_free'
    return field_string


def get_individual_feedback_form(marksheet_type, more_than_one):

    feedback_type = CATEGORIES[marksheet_type]
    number = int(feedback_type['number_of_categories'])

    commenttext = (
        '<div class="col-lg-4 col-md-2 col-sm-2"></div><div ' +
        'class="col-lg-6 col-md-8 col-sm-10">' +
        'For the sake of consistency, please stick ' +
        'to the following general guidelines:<br> Your feedback should be ' +
        'between 150 and 250 words long (currently: <b><span id="wc">0' +
        '</span> words</b>).<br>' +
        'Make sure you address the following issues:<br>' +
        '<ol><li><strong>C</strong>ontent</li>' +
        '<li><strong>R</strong>esearch</li>' +
        '<li><strong>A</strong>nalysis</li>' +
        '<li><strong>A</strong>pplication</li>' +
        '<li><strong>P</strong>resentation</li></ol></div>'
    )
    last_sentence = (
        '<div class="col-lg-4 col-md-2 col-sm-2"></div><div ' +
        'class="col-lg-6 col-md-8 col-sm-10">' +
        'The following sentence will be added at the end of the feedback:' +
        ' <div id="last_sentence">For further feedback, please see '
    )
    if more_than_one:
        last_sentence += 'one of us in their '
    else:
        last_sentence += 'me in my '
    last_sentence += 'office hour.</div></div><br>'

    class IndividualFeedbackForm(forms.ModelForm):
        mark = forms.IntegerField(
            validators=[MaxValueValidator(100), MinValueValidator(0)]
        )
        helper = FormHelper()
        submission_date_helptext = (
            '<span class="glyphicon glyphicon-question-sign" data-toggle=' +
            '"tooltip" data-placement="bottom" data-html="true" title="' +
            'The date of the electronic submission is the relevant one' +
            '"></span>'
        )
        if 'two_comment_parts' in feedback_type:
            if feedback_type['two_comment_parts'] == True:
                if number == 3:
                    helper.layout = Layout(
                        Field('markers', css_class='chosen-select'),
                        Field('marking_date', css_class='datepicker'),
                        # The Prepended text for submission_date doesn't
                        # prepend
                        PrependedText(
                            Field('submission_date', css_class='datepicker'),
                            submission_date_helptext
                        ),
                        PrependedText(
                            fieldname(marksheet_type, 1),
                            get_helptext_html(marksheet_type, 1)
                        ),
                        HTML('<div id="error_1" class="has-error"></div>'),
                        PrependedText(
                            fieldname(marksheet_type, 2),
                            get_helptext_html(marksheet_type, 2)
                        ),
                        HTML('<div id="error_2" class="has-error"></div>'),
                        PrependedText(
                            fieldname(marksheet_type, 3),
                            get_helptext_html(marksheet_type, 3)
                        ),
                        HTML('<div id="error_3" class="has-error"></div>'),
                        HTML(commenttext),
                        Field('comments'),
                        Field('comments_2'),
                        HTML('<div class="col-lg-4 col-md-2 col-sm-2"></div>' +
                                '<div class="col-lg-6 col-md-8 col-sm-10">' +
                                '<p id="penalty_suggestion" ' +
                                'class="text-warning"></p></div>'
                        ),
                        'mark',
                        HTML(last_sentence),
                        FormActions(
                            Submit(
                                'save', 'Save', css_class="btn btn-primary")
                        )
                    )
                elif number == 4:
                    helper.layout = Layout(
                        Field('markers', css_class='chosen-select'),
                        Field('marking_date', css_class='datepicker'),
                        PrependedText(
                            Field('submission_date', css_class='datepicker'),
                            submission_date_helptext
                        ),
                        PrependedText(
                            fieldname(marksheet_type, 1),
                            get_helptext_html(marksheet_type, 1)
                        ),
                        HTML('<div id="error_1" class="has-error"></div>'),
                        PrependedText(
                            fieldname(marksheet_type, 2),
                            get_helptext_html(marksheet_type, 2)
                        ),
                        HTML('<div id="error_2" class="has-error"></div>'),
                        PrependedText(
                            fieldname(marksheet_type, 3),
                            get_helptext_html(marksheet_type, 3)
                        ),
                        HTML('<div id="error_3" class="has-error"></div>'),
                        PrependedText(
                            fieldname(marksheet_type, 4),
                            get_helptext_html(marksheet_type, 4)
                        ),
                        HTML('<div id="error_4" class="has-error"></div>'),
                        HTML(commenttext),
                        Field('comments'),
                        Field('comments_2'),
                        HTML('<div class="col-lg-4 col-md-2 col-sm-2"></div>' +
                                '<div class="col-lg-6 col-md-8 col-sm-10">' +
                                '<p id="penalty_suggestion" ' +
                                'class="text-warning"></p></div>'
                        ),
                        'mark',
                        HTML(last_sentence),
                        FormActions(
                            Submit(
                                'save', 'Save', css_class="btn btn-primary")
                        )
                    )
        else:
            if number == 3:
                helper.layout = Layout(
                    Field('markers', css_class='chosen-select'),
                    Field('marking_date', css_class='datepicker'),
                    # The Prepended text for submission_date doesn't prepend
                    PrependedText(
                        Field('submission_date', css_class='datepicker'),
                        submission_date_helptext
                    ),
                    PrependedText(
                        fieldname(marksheet_type, 1),
                        get_helptext_html(marksheet_type, 1)
                    ),
                    HTML('<div id="error_1" class="has-error"></div>'),
                    PrependedText(
                        fieldname(marksheet_type, 2),
                        get_helptext_html(marksheet_type, 2)
                    ),
                    HTML('<div id="error_2" class="has-error"></div>'),
                    PrependedText(
                        fieldname(marksheet_type, 3),
                        get_helptext_html(marksheet_type, 3)
                    ),
                    HTML('<div id="error_3" class="has-error"></div>'),
                    HTML(commenttext),
                    'comments',
                    HTML('<div class="col-lg-4 col-md-2 col-sm-2"></div>' +
                            '<div class="col-lg-6 col-md-8 col-sm-10">' +
                            '<p id="penalty_suggestion" ' +
                            'class="text-warning"></p></div>'
                    ),
                    'mark',
                    HTML(last_sentence),
                    FormActions(
                        Submit(
                            'save', 'Save', css_class="btn btn-primary")
                    )
                )
            elif number == 4:
                helper.layout = Layout(
                    Field('markers', css_class='chosen-select'),
                    Field('marking_date', css_class='datepicker'),
                    PrependedText(
                        Field('submission_date', css_class='datepicker'),
                        submission_date_helptext
                    ),
                    PrependedText(
                        fieldname(marksheet_type, 1),
                        get_helptext_html(marksheet_type, 1)
                    ),
                    HTML('<div id="error_1" class="has-error"></div>'),
                    PrependedText(
                        fieldname(marksheet_type, 2),
                        get_helptext_html(marksheet_type, 2)
                    ),
                    HTML('<div id="error_2" class="has-error"></div>'),
                    PrependedText(
                        fieldname(marksheet_type, 3),
                        get_helptext_html(marksheet_type, 3)
                    ),
                    HTML('<div id="error_3" class="has-error"></div>'),
                    PrependedText(
                        fieldname(marksheet_type, 4),
                        get_helptext_html(marksheet_type, 4)
                    ),
                    HTML('<div id="error_4" class="has-error"></div>'),
                    HTML(commenttext),
                    Field('comments'),
                    HTML('<div class="col-lg-4 col-md-2 col-sm-2"></div>' +
                            '<div class="col-lg-6 col-md-8 col-sm-10">' +
                            '<p id="penalty_suggestion" ' +
                            'class="text-warning"></p></div>'
                    ),
                    'mark',
                    HTML(last_sentence),
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
                if feedback_type['title'] == (
                        'Assessed Negotiation and Critical Reflection'):
                    self.fields['comments'].label = 'Comments on negotiation'
                    self.fields['comments_2'].label = (
                        'Comments on written work')

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
            if 'two_comment_parts' in feedback_type:
                if feedback_type['two_comment_parts'] == True:
                    fields.append('comments_2')

    return IndividualFeedbackForm


def get_individual_feedback_form_for_group(marksheet_type):

    feedback_type = CATEGORIES[marksheet_type]
    number = int(feedback_type['number_of_individual_categories'])

    class IndividualFeedbackForm(forms.ModelForm):
        helper = FormHelper()
        if number == 3:
            helper.layout = Layout(
                PrependedText(
                    fieldname(marksheet_type, 1),
                    get_helptext_html(marksheet_type, 1)
                ),
                HTML('<div id="error_1" class="has-error"></div>'),
                PrependedText(
                    fieldname(marksheet_type, 2),
                    get_helptext_html(marksheet_type, 2)
                ),
                HTML('<div id="error_2" class="has-error"></div>'),
                PrependedText(
                    fieldname(marksheet_type, 3),
                    get_helptext_html(marksheet_type, 3)
                ),
                HTML('<div id="error_3" class="has-error"></div>'),
                'comments',
                Field('individual_mark', css_class='individual_mark')
            )
        elif number == 4:
            helper.layout = Layout(
                PrependedText(
                    fieldname(marksheet_type, 1),
                    get_helptext_html(marksheet_type, 1)
                ),
                HTML('<div id="error_1" class="has-error"></div>'),
                PrependedText(
                    fieldname(marksheet_type, 2),
                    get_helptext_html(marksheet_type, 2)
                ),
                HTML('<div id="error_2" class="has-error"></div>'),
                PrependedText(
                    fieldname(marksheet_type, 3),
                    get_helptext_html(marksheet_type, 3)
                ),
                HTML('<div id="error_3" class="has-error"></div>'),
                PrependedText(
                    fieldname(marksheet_type, 4),
                    get_helptext_html(marksheet_type, 4)
                ),
                HTML('<div id="error_4" class="has-error"></div>'),
                'comments',
                'individual_mark',
            )
        # helper.form_class = "form-horizontal"
        # helper.label_class = "col-lg-4 col-md-2 col-sm-2"
        # helper.field_class = "col-lg-6 col-md-8 col-sm-10"
        helper.form_tag = False
        helper.disable_csrf = True

        def __init__(self, *args, **kwargs):
            super(IndividualFeedbackForm, self).__init__(*args, **kwargs)
            for x in range(1, number + 1):
                field_name = fieldname(marksheet_type, x)
                labelname = 'i-' + str(x)
                self.fields[field_name].label = feedback_type[labelname]

        class Meta:
            model = IndividualFeedback
            fields = [
                'comments',
                'individual_mark',
            ]
            for x in range(1, number + 1):
                fields.append(fieldname(marksheet_type, x))

    return IndividualFeedbackForm


def get_group_feedback_form(marksheet_type):

    feedback_type = CATEGORIES[marksheet_type]
    number = int(feedback_type['number_of_group_categories'])

    class GroupFeedbackForm(forms.ModelForm):
        helper = FormHelper()
        if number == 2:
            helper.layout = Layout(
                Field('markers', css_class='chosen-select'),
                Field('marking_date', css_class='datepicker'),
                Field('submission_date', css_class='datepicker'),
                PrependedText(
                    fieldname(marksheet_type, 1, group=True),
                    get_helptext_html(marksheet_type, 1, group=True)
                ),
                HTML('<div id="error_1" class="has-error"></div>'),
                PrependedText(
                    fieldname(marksheet_type, 2, group=True),
                    get_helptext_html(marksheet_type, 2, group=True)
                ),
                HTML('<div id="error_2" class="has-error"></div>'),
                'comments',
                HTML('<div class="col-lg-4 col-md-2 col-sm-2"></div>' +
                        '<div class="col-lg-6 col-md-8 col-sm-10">' +
                        '<p id="penalty_suggestion" class="text-warning">' +
                        '</p></div><br>'
                ),
                'group_mark',
                HTML('<div id="group-mark_error" class="has-error"></div>'),

            )
        if number == 3:
            helper.layout = Layout(
                Field('markers', css_class='chosen-select'),
                Field('marking_date', css_class='datepicker'),
                Field('submission_date', css_class='datepicker'),
                PrependedText(
                    fieldname(marksheet_type, 1, group=True),
                    get_helptext_html(marksheet_type, 1, group=True)
                ),
                HTML('<div id="error_1" class="has-error"></div>'),
                PrependedText(
                    fieldname(marksheet_type, 2, group=True),
                    get_helptext_html(marksheet_type, 2, group=True)
                ),
                HTML('<div id="error_2" class="has-error"></div>'),
                PrependedText(
                    fieldname(marksheet_type, 3, group=True),
                    get_helptext_html(marksheet_type, 3, group=True)
                ),
                HTML('<div id="error_3" class="has-error"></div>'),
                'comments',
                HTML('<div class="col-lg-4 col-md-2 col-sm-2"></div>' +
                        '<div class="col-lg-6 col-md-8 col-sm-10">' +
                        '<p id="penalty_suggestion" class="text-warning">' +
                        '</p></div><br>'
                ),
                'group_mark'
            )
        # helper.form_class = "form-horizontal"
        # helper.label_class = "col-lg-4 col-md-2 col-sm-2"
        # helper.field_class = "col-lg-6 col-md-8 col-sm-10"
        helper.form_tag = False
        helper.disable_csrf = True

        def __init__(self, *args, **kwargs):
            super(GroupFeedbackForm, self).__init__(*args, **kwargs)
            for x in range(1, number + 1):
                field_name = fieldname(marksheet_type, x, group=True)
                labelname = 'g-' + str(x)
                self.fields[field_name].label = feedback_type[labelname]

        class Meta:
            model = GroupFeedback
            fields = [
                'markers',
                'marking_date',
                'submission_date',
                'comments',
                'group_mark',
            ]
            for x in range(1, number + 1):
                fields.append(fieldname(marksheet_type, x, group=True))

    return GroupFeedbackForm
