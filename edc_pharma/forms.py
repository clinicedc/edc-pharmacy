
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, ButtonHolder
from django.urls.base import reverse
from django.core.validators import RegexValidator

from edc_pharma.models import TABLET, SYRUP, IV


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


class DispenseForm(forms.ModelForm):
    def clean(self):
        if self.data['dispense_type'] == TABLET:
            self.validate_tablet()
        elif self.data['dispense_type'] == SYRUP:
            self.validate_syrup()
        elif self.data['dispense_type'] == IV:
            self.validate_iv()
        return self.cleaned_data

    def validate_tablet(self):
        if self.data['number_of_teaspoons']:
            raise forms.ValidationError("You have selected dispense type tablet, you should NOT enter number of teaspoons")
        if not self.data['number_of_tablets']:
            raise forms.ValidationError("You have selected dispense type tablet, you should enter number of tablets")
        if self.data['total_dosage_volume']:
            raise forms.ValidationError("You have selected dispense type tablet, you should NOT enter total dosage volume")
        if self.data['iv_duration']:
            raise forms.ValidationError("You have selected dispense type tablet, you should NOT enter IV duration")
        if not self.data['total_number_of_tablets']:
            raise forms.ValidationError("You have selected dispense type tablet, you should enter total number of tablets")

    def validate_syrup(self):
        if not self.data['number_of_teaspoons']:
            raise forms.ValidationError("You have selected dispense type syrup, you should enter number of teaspoons")
        if self.data['number_of_tablets']:
            raise forms.ValidationError("You have selected dispense type syrup, you should NOT enter number of tablets")
        if self.data['total_number_of_tablets']:
            raise forms.ValidationError("You have selected dispense type syrup, you should NOT enter total number of tablets")
        if not self.data['total_dosage_volume']:
            raise forms.ValidationError("You have selected dispense type syrup, you should enter total dosage volume")
        if self.data['iv_duration']:
            raise forms.ValidationError("You have selected dispense type syrup, you should NOT enter  IV duration")

    def validate_iv(self):
        if self.data['number_of_teaspoons']:
            raise forms.ValidationError("You have selected dispense type IV, you should NOT enter number of teaspoons")
        if self.data['number_of_tablets']:
            raise forms.ValidationError("You have selected dispense type IV, you should NOT enter number of tablets")
        if not self.data['total_dosage_volume']:
            raise forms.ValidationError("You have selected dispense type IV, you should enter total dosage volume")
        if not self.data['iv_duration']:
            raise forms.ValidationError("You have selected dispense type IV, you should enter IV duration")
