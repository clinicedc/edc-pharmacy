from edc_pharma.models import Prescription, DispenseAppointment, WorkList

from django import forms


class DispenseAppointmentForm(forms.ModelForm):

    class Meta:
        model = DispenseAppointment
        fields = '__all__'


class PrescriptionForm(forms.ModelForm):

    class Meta:
        model = Prescription
        fields = '__all__'


class WorklistForm(forms.ModelForm):

    class Meta:
        model = WorkList
        fields = '__all__'
