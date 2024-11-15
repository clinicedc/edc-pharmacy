from django.db import models
from django.db.models import PROTECT
from edc_model.models import BaseUuidModel, HistoricalRecords
from sequences import get_next_value

from ...exceptions import LotError
from ..medication import Assignment
from .product import Product


class Manager(models.Manager):
    use_in_migrations = True


class Lot(BaseUuidModel):

    lot_identifier = models.CharField(
        max_length=25,
        unique=True,
        null=True,
        blank=False,
        help_text="A sequential unique identifier set by the EDC",
    )

    lot_no = models.CharField(max_length=50, unique=True)

    product = models.ForeignKey(Product, on_delete=PROTECT, null=True, blank=False)

    assignment = models.ForeignKey(Assignment, on_delete=models.PROTECT, null=True, blank=True)

    expiration_date = models.DateField()

    objects = Manager()

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.lot_no}: {self.product.name} "

    def save(self, *args, **kwargs):
        if not self.lot_identifier:
            self.lot_identifier = f"{get_next_value(self._meta.label_lower):06d}"
        if self.assignment != self.product.assignment:
            raise LotError("Assignment mismatch.")
        super().save(*args, **kwargs)

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Lot"
        verbose_name_plural = "Lots"