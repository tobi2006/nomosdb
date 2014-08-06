from django import forms
from database.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from crispy_forms.bootstrap import TabHolder, Tab, FormActions

NO_STUDENT_ID_ERROR = "You need to specify a unique student ID number"

class StudentForm(forms.ModelForm):
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
    helper.form_class="form-horizontal"
    helper.label_class="col-lg-2"
    helper.field_class="col-lg-6 col-md-8 col-sm-10"

    class Meta:
        model = Student
        error_messages = {
            'student_id': {'required': NO_STUDENT_ID_ERROR}
        }
