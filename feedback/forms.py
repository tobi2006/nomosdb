from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Fieldset, HTML, Div
from crispy_forms.bootstrap import TabHolder, Tab, FormActions
from main.models import *

class IndividualFeedbackForm(forms.Form):
    markers = []
    for teacher in Staff.objects.filter(role='teacher'):
        if teacher.
    marker = forms.CharField(label="Current Year", required=True)
