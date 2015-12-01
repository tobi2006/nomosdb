from django import forms
from main.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Fieldset, HTML, Div
from crispy_forms.bootstrap import TabHolder, Tab, FormActions
from main.unisettings import TEACHING_WEEK_HELPTEXT, TEACHING_WEEK_OPTIONS

NO_STUDENT_ID_ERROR = "You need to specify a unique student ID number"


class MainSettingsForm(forms.Form):
    """The form for all the main settings"""
    current_year = forms.CharField(label="Current Year", required=True)
    uni_name = forms.CharField(label="Name of the University", required=True)
    uni_short_name = forms.CharField(
        label="Short name for the University", required=True)
    nomosdb_url = forms.CharField(
        label="URL for this Data System", required=True)
    admin_name = forms.CharField(
        label="Name of the admin for signing emails (could be a team as well)",
        required=True
    )
    admin_email = forms.CharField(
        label="Email of the admin team", required=True)
    example_email = forms.CharField(
        label="Example Email for a user", required=True
    )
    helper = FormHelper()
    helper.layout = Layout(
        'current_year',
        'uni_name',
        'uni_short_name',
        'nomosdb_url',
        'admin_name',
        'admin_email',
        'example_email',
        FormActions(
            Submit('save', 'Save Settings', css_class="btn btn-primary")
        )
    )
    helper.form_class = "form-horizontal"
    helper.label_class = "col-lg-4 col-md-2 col-sm-2"
    helper.field_class = "col-lg-6 col-md-8 col-sm-10"


class SubjectAreaForm(forms.ModelForm):
    """The modelform for the subject area - very simple"""

    class Meta:
        fields = ['name']
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
        fields = ['title', 'short_title', 'subject_areas']


class AssessmentForm(forms.ModelForm):
    """The modelform for assessments, using crispy forms"""
    helper = FormHelper()
    helper.layout = Layout(
        'title',
        'value',
        HTML('<div id="error" class="has-error"></div>'),
        HTML('<h4>First Attempt</h4>'),
        Field(
            'submission_date',
            placeholder='Leave blank if not applicable',
            css_class="datepicker",
        ),
        Field('max_word_count', placeholder='Leave blank if not applicable'),
        'marksheet_type',
        'co_marking',
        'group_assessment',
        'same_marksheet_for_all',
        HTML('<h4>Resits</h4>'),
        Field(
            'resit_submission_date',
            placeholder='Leave blank if not applicable',
            css_class="datepicker",
        ),
        Field(
            'resit_max_word_count',
            placeholder='Leave blank if not applicable'
        ),
        'resit_marksheet_type',
        'resit_co_marking',
        'resit_group_assessment',
        'resit_same_marksheet_for_all',
        FormActions(
            Submit('save', 'Save Assessment', css_class="btn btn-primary")
        )
    )
    helper.form_class = "form-horizontal"
    helper.label_class = "col-lg-2"
    helper.field_class = "col-lg-6 col-md-8 col-sm-10"

    class Meta:
        model = Assessment
        fields = [
            'title',
            'value',
            'submission_date',
            'resit_submission_date',
            'max_word_count',
            'resit_max_word_count',
            'marksheet_type',
            'resit_marksheet_type',
            'co_marking',
            'resit_co_marking',
            'group_assessment',
            'resit_group_assessment',
            'same_marksheet_for_all',
            'resit_same_marksheet_for_all'
        ]


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
                'tutor',
                'is_part_time',
                'second_part_time_year',
                'since',
                'qld',
                'tier_4',
                'active',
            ),
            Tab(
                'Contact Information',
                'permanent_email',
                'phone_number',
                'cell_number',
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
        exclude = [
            'modules',
            'nalp',
            'achieved_degree',
            'graduated_in',
            'user'
        ]
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
                Field('teachers', css_class='chosen-select'),
                'credits',
                # 'sucessor_of',
                'eligible',
                'foundational',
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
        fields = [
            'title',
            'code',
            'year',
            'teachers',
            'subject_areas',
            'credits',
            'eligible',
            'foundational',
            'first_session',
            'no_teaching_in',
            'last_session'
        ]


class StaffForm(forms.Form):
    """A form for staff members, to be used by admins"""
    choices = []
    queryset = SubjectArea.objects.all()
    for area in queryset:
        tpl = (area.slug, area.name)
        choices.append(tpl)
    choices = tuple(choices)
    ROLES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
    )
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    email = forms.EmailField(label="Email Address", required=True)
    subject_areas = forms.MultipleChoiceField(required=False, choices=choices)
    role = forms.ChoiceField(choices=ROLES)
    helper = FormHelper()
    helper.form_method = "POST"
    helper.layout = Layout(
        'first_name',
        'last_name',
        'email',
        Field('subject_areas', css_class='chosen-select'),
        'role',
        FormActions(
            Submit('save', 'Save Staff Member', css_class='btn btn-primary'))
    )
    helper.form_class = "form-horizontal"
    helper.label_class = "col-lg-2"
    helper.field_class = "col-lg-6 col-md-8 col-sm-10"


class TuteeSessionForm(forms.ModelForm):
    """The form to enter tutee sessions"""
    helper = FormHelper()
    helper.layout = Layout(
        Field(
            'date_of_meet',
            css_class="datepicker",
        ),
        'meeting_took_place',
        'notes',
        FormActions(
            Submit('save', 'Save Session', css_class="btn btn-primary")
        )
    )

    class Meta:
        model = TuteeSession
        fields = ['date_of_meet', 'meeting_took_place', 'notes']


class CSVUploadForm(forms.Form):
    csvfile = forms.FileField(
        label='Select a .csv file',
        help_text=("Simply save the spreadsheet under Excel or LibreOffice " +
                   "as a .csv File (either under Save As or under Export")
    )
