from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, ButtonHolder
from django.urls.base import reverse
from django.core.validators import RegexValidator


class PatientForm(forms.Form):

    subject_identifier = forms.CharField(
        label='Patient Identifier',
        # validators=[RegexValidator(r'[0-9]')],
        max_length=36)

    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper = FormHelper()
        self.helper.form_action = reverse('home_url')
        self.helper.form_id = 'form-patient-search'
        self.helper.form_method = 'post'
        self.helper.html5_required = True
        self.helper.layout = Layout(
            'subject_identifier',
            ButtonHolder(
                Submit('submit', 'Search', css_class="pull-right"),
            ))
