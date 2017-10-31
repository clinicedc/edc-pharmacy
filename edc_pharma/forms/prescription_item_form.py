from django import forms

from ..dosage_calculator import DosageCalculator
from ..models import PrescriptionItem


class PrescriptionItemForm(forms.ModelForm):

    #     dose_calculator = DosageCalculator()
    #
    #     def clean(self):
    #         cleaned_data = super().clean()
    #         if not cleaned_data.get('dose'):
    #             cleaned_data['dose'] = self.dose_calculator.get_dose(
    #                 subject_identifier=cleaned_data.get(
    #                     'prescription').subject_identifier,
    #                 medication=cleaned_data.get('medication')
    #             )
    #         return cleaned_data

    class Meta:
        model = PrescriptionItem
        fields = '__all__'
