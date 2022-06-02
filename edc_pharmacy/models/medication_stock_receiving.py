from django.db import models
from django.db.models import PROTECT
from edc_model import models as edc_models

from .medication_product import MedicationProduct


class Manager(models.Manager):

    use_in_migrations = True


class MedicationStockReceiving(edc_models.BaseUuidModel):

    medication_product = models.ForeignKey(MedicationProduct, on_delete=PROTECT)

    qty = models.IntegerField()

    stock_identifiers = models.TextField()

    received = models.BooleanField(default=False)

    received_datetime = models.DateTimeField(null=True, blank=True)

    objects = Manager()

    history = edc_models.HistoricalRecords()

    def __str__(self):
        return f"{self.medication_product}: {self.qty} recv'd on {self.received_datetime}"

    class Meta(edc_models.BaseUuidModel.Meta):
        verbose_name = "Medication stock: Receiving"
        verbose_name_plural = "Medication stock: Receiving"
