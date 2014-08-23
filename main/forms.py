from django import forms
from main.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Fieldset, HTML, Div
from crispy_forms.bootstrap import TabHolder, Tab, FormActions
from nomosdb.unisettings import TEACHING_WEEK_HELPTEXT, TEACHING_WEEK_OPTIONS

NO_STUDENT_ID_ERROR = "You need to specify a unique student ID number"


class SubjectAreaForm(forms.ModelForm):
    """The modelform for the subject area - very simple"""

    class Meta:
        model = SubjectArea
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}


class CourseForm(forms.ModelForm):
    """the modelform for the course model, using crispy forms"""
    helper = FormHelper()
    helper.layout = Layout(
        'title',
        'short_title',
        Field('subject_areas', css_class='chosen-select'),
        FormActions(
            Submit('save', 'Save Course', css_class="btn btn-primary")
        )
    )
    helper.form_class = "form-horizontal"
    helper.label_class = "col-lg-2"
    helper.field_class = "col-lg-6 col-md-8 col-sm-10"

    class Meta:
        model = Course


class AssessmentForm(forms.ModelForm):
    """The modelform for assessments, using crispy forms"""
    helper = FormHelper()
    helper.layout = Layout(
        'title',
        'value',
        HTML('<div id="error" class="has-error"></div>'),
        'submission_date',
        'max_word_count',
        # 'marksheet_type',
        FormActions(
            Submit('save', 'Save Assessment', css_class="btn btn-primary")
        )
    )
    helper.form_class = "form-horizontal"
    helper.label_class = "col-lg-2"
    helper.field_class = "col-lg-6 col-md-8 col-sm-10"

    class Meta:
        model = Assessment


class StudentForm(forms.ModelForm):
    """The modelform for the student model, using crispy forms"""
    helper = FormHelper()
    helper.layout = Layout(
        TabHolder(
            Tab(
                'Basic Information',
                'student_id',
                'first_name',
                'last_name',
                'email',
                'course',
                'year',
                'is_part_time',
                'second_part_time_year',
                'since',
                'qld',
                'tier_4',
                'nalp',
                'active',
            ),
            Tab(
                'Contact Information',
                'permanent_email',
                'phone_number',
                'address',
                'home_address'
                ),
            Tab(
                'Other Information',
                'lsp',
                'notes',
                'exam_id'
            )
        ),
        FormActions(
            Submit('save', 'Save Student', css_class="btn btn-primary")
        )
    )
    helper.form_class = "form-horizontal"
    helper.label_class = "col-lg-2"
    helper.field_class = "col-lg-6 col-md-8 col-sm-10"

    class Meta:
        model = Student
        error_messages = {
            'student_id': {'required': NO_STUDENT_ID_ERROR}
        }


class ModuleForm(forms.ModelForm):
    """The modelform for the Module model, using crispy forms"""

    # Prepare stuff for second tab (containing the helptext and options)
    if TEACHING_WEEK_HELPTEXT:
        helptext = ('<p>' + TEACHING_WEEK_HELPTEXT + '</p><br>')
    else:
        helptext = ''
    if TEACHING_WEEK_OPTIONS:
        buttons = '<label>Default options: </label><div class="btn-group">'
        numberlist = []
        for number in TEACHING_WEEK_OPTIONS:
            numberlist.append(number)
        numberlist.sort()
        for number in numberlist:
            buttons += '<button type="button" id="option_'
            buttons += str(number)
            buttons += '" class="btn btn-default">'
            buttons += TEACHING_WEEK_OPTIONS[number][0]
            buttons += '</button>'
        buttons += '</div><br><br>'
    else:
        buttons = ''

    helper = FormHelper()
    helper.layout = Layout(
        TabHolder(
            Tab(
                'Module Information',
                'title',
                'code',
                'year',
                Field('subject_areas', css_class='chosen-select'),
                'credits',
                # 'sucessor_of',
                'eligible',
                'foundational',
                'nalp',
            ),
            Tab(
                'Sessions',
                HTML(helptext),
                HTML(buttons),
                'first_session',
                'no_teaching_in',
                'last_session'
            )
        ),
        FormActions(
            Submit('save', 'Save Module', css_class="btn btn-primary")
        )
    )
    helper.form_class = "form-horizontal"
    helper.label_class = "col-lg-2"
    helper.field_class = "col-lg-6 col-md-8 col-sm-10"

    class Meta:
        model = Module
