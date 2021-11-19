from uuid import uuid4

from django.db import models
from django.db.models import PROTECT
from edc_model import models as edc_models
from edc_sites.models import SiteModelMixin

from .medication_product import MedicationProduct


class Manager(models.Manager):

    use_in_migrations = True


class MedicationStock(SiteModelMixin, edc_models.BaseUuidModel):

    stock_identifier = models.CharField(max_length=36, default=uuid4, unique=True)

    medication_product = models.ForeignKey(MedicationProduct, on_delete=PROTECT)

    # TODO: location

    objects = Manager()

    history = edc_models.HistoricalRecords()

    def __str__(self):
        return f"{self.stock_identifier}: {self.medication_product} "

    class Meta(SiteModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Medication stock"
        verbose_name_plural = "Medication stock"
