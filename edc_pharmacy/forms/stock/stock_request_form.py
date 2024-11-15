from django import forms
from edc_registration.models import RegisteredSubject

from ...models import StockRequest


class StockRequestForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("subject_identifiers") and cleaned_data.get(
            "excluded_subject_identifiers"
        ):
            raise forms.ValidationError(
                "Cannot include and exclude subject identifiers in the same request."
            )
        if (
            cleaned_data.get("request_datetime")
            and cleaned_data.get("cutoff_datetime")
            and cleaned_data.get("cutoff_datetime") < cleaned_data.get("request_datetime")
        ):
            raise forms.ValidationError({"cutoff_datetime": "Invalid cutoff date"})
        if cleaned_data.get("subject_identifiers") and cleaned_data.get("location"):
            subject_identifiers = cleaned_data.get("subject_identifiers").split("\n")
            subject_identifiers = [s.strip() for s in subject_identifiers]
            self.cleaned_data["subject_identifiers"] = "\n".join(subject_identifiers)
            if RegisteredSubject.objects.values("subject_identifier").filter(
                subject_identifier__in=subject_identifiers,
                site_id=cleaned_data.get("location").site_id,
            ).count() != len(subject_identifiers):
                raise forms.ValidationError(
                    {"subject_identifiers": "Not all subject identifiers are valid."}
                )
        if cleaned_data.get("excluded_subject_identifiers") and cleaned_data.get("location"):
            subject_identifiers = cleaned_data.get("excluded_subject_identifiers").split("\n")
            subject_identifiers = [s.strip() for s in subject_identifiers]
            self.cleaned_data["excluded_subject_identifiers"] = "\n".join(subject_identifiers)
            if RegisteredSubject.objects.values("subject_identifier").filter(
                subject_identifier__in=subject_identifiers,
                site_id=cleaned_data.get("location").site_id,
            ).count() != len(subject_identifiers):
                raise forms.ValidationError(
                    {"excluded_subject_identifiers": "Not all subject identifiers are valid."}
                )
        return cleaned_data

    class Meta:
        model = StockRequest
        fields = "__all__"
        help_text = {"request_identifier": "(read-only)"}
        widgets = {
            "request_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
        }