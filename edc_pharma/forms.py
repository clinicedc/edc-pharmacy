from django import forms

from .models import DispenseAppointment


class DispenseAppointmentForm(forms.ModelForm):

    class Meta:
        model = DispenseAppointment
        fields = '__all__'
