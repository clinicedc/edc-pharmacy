from edc_pharma.models import Prescription, DispenseAppointment

from django import forms


class DispenseAppointmentForm(forms.ModelForm):

    class Meta:
        model = DispenseAppointment
        fields = '__all__'


class PrescriptionForm(forms.ModelForm):

    class Meta:
        model = Prescription
        fields = '__all__'
