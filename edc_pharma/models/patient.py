from datetime import date
from django.core.validators import RegexValidator
from django.db import models

from simple_history.models import HistoricalRecords
from edc_base.model.models import BaseUuidModel
from edc_constants.choices import GENDER
from edc_base.model.validators.date import date_not_future
from edc_base.utils.age import formatted_age

from edc_pharma.models.site import Site


class Patient(BaseUuidModel):

    subject_identifier = models.CharField(max_length=20, unique=True)

    initials = models.CharField(
        max_length=5,
        validators=[RegexValidator('[A-Z]{2,3}', message='Use CAPS, 2-3 letters')],
        help_text='Format is AA or AAA')

    gender = models.CharField(
        max_length=10,
        choices=GENDER)

    dob = models.DateField(
        blank=True,
        null=True,
        validators=[date_not_future])

    sid = models.CharField(
        max_length=20,
        validators=[RegexValidator('[\d]+', 'Invalid format.')],
    )

    consent_date = models.DateTimeField(default=date.today, editable=False)

    site = models.ForeignKey(Site)

    history = HistoricalRecords()

    def __str__(self):
        return '{}, ({}), Site {}'.format(self.subject_identifier, self.initials, self.site.site_code)

    @property
    def born(self):
        return self.dob.strftime('%Y-%m-%d')

    @property
    def age(self):
        return formatted_age(self.dob, date.today())
