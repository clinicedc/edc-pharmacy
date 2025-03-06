from __future__ import annotations

from django.db import models
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_utils import get_utcnow
from sequences import get_next_value

from .storage_bin import StorageBin


class StorageBinItem(BaseUuidModel):
    item_identifier = models.CharField(
        max_length=36,
        unique=True,
        null=True,
        blank=True,
        help_text="A sequential unique identifier set by the EDC",
    )

    storage_bin = models.ForeignKey(StorageBin, on_delete=models.PROTECT)

    stock = models.ForeignKey(
        "edc_pharmacy.stock",
        on_delete=models.PROTECT,
        null=True,
        limit_choices_to={"confirmed_at_site": True, "dispensed": False},
    )

    item_datetime = models.DateTimeField(default=get_utcnow)

    history = HistoricalRecords()

    def __str__(self):
        return (
            f"{self.storage_bin.location.site.id}:"
            f"{self.storage_bin.bin_identifier}:{self.item_identifier}"
        )

    def save(self, *args, **kwargs):
        if not self.id:
            self.item_identifier = f"{get_next_value(self._meta.label_lower):06d}"
        super().save(*args, **kwargs)

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Storage bin item"
        verbose_name_plural = "Storage bin items"
