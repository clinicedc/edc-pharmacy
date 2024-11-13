from django.db import models
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_utils import get_utcnow
from sequences import get_next_value

from ...exceptions import RepackRequestError
from .container import Container


class Manager(models.Manager):
    use_in_migrations = True


class RepackRequest(BaseUuidModel):
    """A model to repack stock from one container into another.

    Move stock from one phycical container into another, for example
    move stock from a bottle of 50000 into x number of containers
    of 128.

    Location is not changed here.
    """

    repack_identifier = models.CharField(
        max_length=36,
        unique=True,
        null=True,
        blank=True,
        help_text="A sequential unique identifier set by the EDC",
    )

    repack_datetime = models.DateTimeField(default=get_utcnow)

    from_stock = models.ForeignKey(
        "edc_pharmacy.stock",
        on_delete=models.PROTECT,
        related_name="repack_requests",
        null=True,
        blank=False,
        limit_choices_to={"repack_request__isnull": True},
    )

    container = models.ForeignKey(
        Container,
        on_delete=models.PROTECT,
        null=True,
        blank=False,
        limit_choices_to={"may_repack_as": True},
    )

    qty = models.DecimalField(
        verbose_name="Quantity", null=True, blank=False, decimal_places=2, max_digits=20
    )

    processed = models.BooleanField(default=False)

    stock_count = models.IntegerField(null=True, blank=True)

    objects = Manager()

    history = HistoricalRecords()

    def __str__(self):
        return self.repack_identifier

    def save(self, *args, **kwargs):
        if not self.repack_identifier:
            next_id = get_next_value(self._meta.label_lower)
            self.repack_identifier = f"{next_id:06d}"
            self.processed = False
        if not self.from_stock.confirmed:
            raise RepackRequestError(
                "Unconfirmed stock item. Only confirmed stock items may "
                "be used to repack. Perhaps catch this in the form"
            )
        super().save(*args, **kwargs)

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Repack request"
        verbose_name_plural = "Repack request"
