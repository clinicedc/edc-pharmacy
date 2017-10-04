from django import forms

from .models import DispenseTimepoint


class DispenseTimepointForm(forms.ModelForm):

    class Meta:
        model = DispenseTimepoint
        fields = '__all__'
