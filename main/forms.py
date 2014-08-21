from django import forms
from main.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Fieldset, HTML, Div
from crispy_forms.bootstrap import TabHolder, Tab, FormActions

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
    helper = FormHelper()
    helper.layout = Layout(
        Fieldset(
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
        FormActions(
            Submit('save', 'Save Module', css_class="btn btn-primary")
        )
    )
    helper.form_class = "form-horizontal"
    helper.label_class = "col-lg-2"
    helper.field_class = "col-lg-6 col-md-8 col-sm-10"

    class Meta:
        model = Module
