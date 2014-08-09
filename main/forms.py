from django import forms
from main.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, HTML, Div
from crispy_forms.bootstrap import TabHolder, Tab, FormActions

NO_STUDENT_ID_ERROR = "You need to specify a unique student ID number"


class SubjectAreaForm(forms.ModelForm):
    """The modelform for the subject area - very simple"""

    class Meta:
        model = SubjectArea


class CourseForm(forms.ModelForm):
    """the modelform for the course model, using crispy forms"""
    helper = FormHelper()
    helper.layout = Layout(
        'title',
        'short_title'
    )
    helper.form_class = "form-horizontal"
    helper.label_class = "col-lg-2"
    helper.field_class = "col-lg-6 col-md-8 col-sm-10"

    class Meta:
        model = Course


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
    helper = FormHelper()
    helper.layout = Layout(
        TabHolder(
            Tab(
                'Module Information',
                'title',
                'code',
                'year',
                'credits',
                # 'sucessor_of',
                'eligible',
                'foundational',
                'nalp',
            ),
            Tab(
                'Attendance',
                'first_session',
                'no_teaching_in',
                'last_session',
            ),
            Tab(
                'Assessment',
                Div(
                    HTML('<h3>Assessment 1</h3>'),
                    'assessment_1_title',
                    'assessment_1_value',
                    'assessment_1_submission_date',
                    'assessment_1_max_word_count',
                    id="assessment_1"
                ),
                Div(
                    HTML('<hr><h3>Assessment 2</h3>'),
                    'assessment_2_title',
                    'assessment_2_value',
                    'assessment_2_submission_date',
                    'assessment_2_max_word_count',
                    id="assessment_2"
                ),
                Div(
                    HTML('<hr><h3>Assessment 3</h3>'),
                    'assessment_3_title',
                    'assessment_3_value',
                    'assessment_3_submission_date',
                    'assessment_3_max_word_count',
                    id="assessment_3"
                ),
                Div(
                    HTML('<hr><h3>Assessment 4</h3>'),
                    'assessment_4_title',
                    'assessment_4_value',
                    'assessment_4_submission_date',
                    'assessment_4_max_word_count',
                    id="assessment_4"
                ),
                Div(
                    HTML('<hr><h3>Assessment 5</h3>'),
                    'assessment_5_title',
                    'assessment_5_value',
                    'assessment_5_submission_date',
                    'assessment_5_max_word_count',
                    id="assessment_5"
                ),
                Div(
                    HTML('<hr><h3>Assessment 6</h3>'),
                    'assessment_6_title',
                    'assessment_6_value',
                    'assessment_6_submission_date',
                    'assessment_6_max_word_count',
                    id="assessment_6"
                ),
                Div(
                    HTML('<hr><h3>Exam</h3>'),
                    'exam_value'
                )
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
