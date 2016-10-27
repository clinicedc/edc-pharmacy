from django.core.validators import RegexValidator
from django.db import models
from simple_history.models import HistoricalRecords

from edc_base.model.models import BaseUuidModel

from edc_pharma.models.protocol import Protocol


class Site(BaseUuidModel):

    history = HistoricalRecords()

    protocol = models.ForeignKey(Protocol)

    site_code = models.CharField(
        max_length=20,
        validators=[RegexValidator('[\d]+', 'Invalid format.')])

    telephone_number = models.CharField(
        max_length=7,
        validators=[RegexValidator('^[2-8]{1}[0-9]{6}$', 'Invalid format.')])

    def __str__(self):
        return '{}, Protocol: {}'.format(self.site_code, self.protocol)
