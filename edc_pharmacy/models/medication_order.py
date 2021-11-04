from django.db import models
from django.db.models import PROTECT
from edc_model.models import BaseUuidModel
from edc_sites.models import SiteModelMixin

from .dosage_guideline import DosageGuideline
from .formulation import Formulation
from .rx import Rx


class MedicationOrder(SiteModelMixin, BaseUuidModel):

    rx = models.ForeignKey(Rx, on_delete=PROTECT)

    dosage_guideline = models.ForeignKey(DosageGuideline, on_delete=PROTECT)

    formulation = models.ForeignKey(Formulation, on_delete=PROTECT)

    packed = models.BooleanField(default=False)

    shipped = models.BooleanField(default=False)

    received = models.BooleanField(default=False)

    class Meta(BaseUuidModel.Meta):
        pass
