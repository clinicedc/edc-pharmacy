
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators.date import datetime_not_future

from django.db import models

from edc_search.model_mixins import SearchSlugModelMixin


class WorkList(SearchSlugModelMixin, BaseUuidModel):

    """A model linked to the subject consent to record corrections.
    """

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50,
        unique=True)

    report_datetime = models.DateTimeField(
        verbose_name="Report Datetime",
        null=True,
        validators=[
            datetime_not_future],
    )

    next_dispensing_datetime = models.DateTimeField(
        verbose_name="Next Dispensing Datetime",
        null=True,
        validators=[
            datetime_not_future],
    )

    enrollment_datetime = models.DateTimeField(
        verbose_name="Next Dispensing Datetime",
        null=True,
        validators=[
            datetime_not_future],
    )

    status = models.CharField(
        verbose_name="Status",
        max_length=50)

    def __str__(self):
        return str(self.subject_identifier,)

    def get_search_slug_fields(self):
        fields = ['subject_identifier']
        return fields

    class Meta:
        app_label = 'edc_pharma'
