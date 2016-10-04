from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from datetime import date
from django import forms
from django.urls.base import reverse
from django.db.models import Q
from edc_pharma.models import TABLET, SYRUP, IV
from .models import Dispense


class PatientForm(forms.Form):

    subject_identifier = forms.CharField(
        label='Patient Identifier',
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
            FieldWithButtons('subject_identifier', StrictButton('Search', type='submit')))


class DispenseForm(forms.ModelForm):

    def clean(self):
        if self.data['dispense_type'] == TABLET:
            self.validate_tablet()
        elif self.data['dispense_type'] == SYRUP:
            self.validate_syrup()
        elif self.data['dispense_type'] == IV:
            self.validate_iv()
        else:
            pass
        self.catch_unique_integrity_error()
        return self.cleaned_data

    def catch_unique_integrity_error(self):
        if Dispense.objects.filter(
                Q(patient=self.cleaned_data['patient']) &
                Q(medication=self.cleaned_data['medication']) &
                Q(prepared_date=date.today())):
            raise forms.ValidationError('Dispense record of this medication on this date already exists for this patient')
        return self.cleaned_data

    def validate_tablet(self):
        if self.data['syrup_volume']:
            raise forms.ValidationError({
                'syrup_volume': [
                    'You have selected dispense type tablet, you should NOT enter syrup volume']})
        if not self.data['number_of_tablets']:
            raise forms.ValidationError({
                'number_of_tablets': [
                    'You have selected dispense type tablet, you should enter number of tablets']})
        if self.data['total_dosage_volume']:
            raise forms.ValidationError({
                'total_dosage_volume': [
                    'You have selected dispense type tablet, you should NOT enter total dosage volume']})
        if self.data['iv_duration']:
            raise forms.ValidationError({
                'iv_duration': [
                    'You have selected dispense type tablet, you should NOT enter IV duration']})
        if not self.data['total_number_of_tablets']:
            raise forms.ValidationError({
                'total_number_of_tablets': [
                    'You have selected dispense type tablet, you should enter total number of tablets']})
        if not self.data['times_per_day']:
            raise forms.ValidationError({
                'times_per_day': [
                    'You have selected dispense type tablet, you should enter times per day']})
        if self.data['iv_concentration']:
            raise forms.ValidationError({
                'iv_concentration': [
                    'You have selected dispense type tablet, you should NOT enter IV concentration']})
        if float(self.data['total_number_of_tablets']) < float(self.data['times_per_day']) * float(self.data['number_of_tablets']):
            raise forms.ValidationError({
                'total_number_of_tablets': [
                    'Cannot have total number of tablets less than number of tablets by times per day']})

    def validate_syrup(self):
        if not self.data['syrup_volume']:
            raise forms.ValidationError({
                'syrup_volume': [
                    'You have selected dispense type syrup, you should enter syrup volume']})
        if self.data['number_of_tablets']:
            raise forms.ValidationError({
                'number_of_tablets': [
                    'You have selected dispense type syrup, you should NOT enter number of tablets']})
        if self.data['total_number_of_tablets']:
            raise forms.ValidationError({
                'total_number_of_tablets': [
                    'You have selected dispense type syrup, you should NOT enter total number of tablets']})
        if not self.data['total_dosage_volume']:
            raise forms.ValidationError({
                'total_dosage_volume': [
                    'You have selected dispense type syrup, you should enter total dosage volume']})
        if self.data['iv_duration']:
            raise forms.ValidationError({
                'iv_duration': [
                    'You have selected dispense type syrup, you should NOT enter IV duration']})
        if self.data['iv_concentration']:
            raise forms.ValidationError({
                'iv_concentration': [
                    'You have selected dispense type syrup, you should NOT enter IV concentration']})
        if not self.data['times_per_day']:
            raise forms.ValidationError({
                'times_per_day': [
                    'You have selected dispense type syrup, you should enter times per day']})

    def validate_iv(self):
        if self.data['syrup_volume']:
            raise forms.ValidationError({
                'syrup_volume': [
                    'You have selected dispense type IV, you should NOT enter syrup volume']})
        if self.data['number_of_tablets']:
            raise forms.ValidationError({
                'number_of_tablets': [
                    'You have selected dispense type IV, you should NOT enter number of tablets']})
        if not self.data['total_dosage_volume']:
            raise forms.ValidationError({
                'total_dosage_volume': [
                    'You have selected dispense type IV, you should enter total dosage volume']})
        if not self.data['iv_duration']:
            raise forms.ValidationError({
                'iv_duration': [
                    'You have selected dispense type IV, you should enter IV duration']})
        if not self.data['iv_concentration']:
            raise forms.ValidationError({
                'iv_concentration': [
                    'You have selected dispense type IV, you should enter IV concentration']})
        if self.data['total_number_of_tablets']:
            raise forms.ValidationError({
                'total_number_of_tablets': [
                    'You have selected dispense type IV, you should NOT enter total number of tablets']})
        if self.data['times_per_day']:
            raise forms.ValidationError({
                'times_per_day': [
                    'You have selected dispense type IV, you should NOT enter times per day']})

    class Meta:
        model = Dispense
        fields = '__all__'
