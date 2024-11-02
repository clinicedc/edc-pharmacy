from django.db import models
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_utils import get_utcnow
from edc_utils.date import to_local
from sequences import get_next_value

from ..storage import Location
from .order import Order


class Manager(models.Manager):
    use_in_migrations = True


class Receive(BaseUuidModel):

    receive_identifier = models.CharField(max_length=36, unique=True, null=True, blank=True)

    receive_datetime = models.DateTimeField(default=get_utcnow)

    item_count = models.IntegerField(verbose_name="Item count", null=True)

    location = models.ForeignKey(Location, on_delete=models.PROTECT)

    order = models.ForeignKey(Order, on_delete=models.PROTECT)

    objects = Manager()

    history = HistoricalRecords()

    def __str__(self):
        return (
            f"{self.receive_identifier}:{self.order}: "
            f"recv'd on {to_local(self.receive_datetime).date()}"
        )

    def save(self, *args, **kwargs):
        if not self.receive_identifier:
            self.receive_identifier = f"{get_next_value(self._meta.label_lower):06d}"
        super().save(*args, **kwargs)

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Stock: Receive"
        verbose_name_plural = "Stock: Receive"