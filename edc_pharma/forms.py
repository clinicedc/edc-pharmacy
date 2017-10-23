from edc_pharma.models import Prescription, DispenseAppointment, WorkList

from django import forms


class DispenseAppointmentForm(forms.ModelForm):

    class Meta:
        model = DispenseAppointment
        fields = '__all__'


class PrescriptionForm(forms.ModelForm):

    subject_identifier = forms.CharField(
        label='Screening identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    arm = forms.CharField(
        label='Randomization Arm',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    result = forms.CharField(
        label='Auto calculated required quantity',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Prescription
        fields = '__all__'


class WorklistForm(forms.ModelForm):

    class Meta:
        model = WorkList
        fields = '__all__'
