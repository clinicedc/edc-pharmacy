from django.db import models
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_utils import get_utcnow
from sequences import get_next_value

from ...exceptions import RepackRequestError
from ..proxy_models import LabelSpecificationProxy
from .container import Container


class Manager(models.Manager):
    use_in_migrations = True


class RepackRequest(BaseUuidModel):
    """A model to repack stock from one container into another.

    Move stock from one container into another, for example
    move stock from a bottle of 50000 into x number of containers
    of 128.

    On save, populate stock with `QTY` new records. Stock is flagged
    as confirmed=False until label scanned into edc

    stock_identifier:
        You can specify the source container by stock identifier or
        leave stock_identifier to let the EDC decide which stock item
        or items to draw from. EDC will choose by ascending order of
        the stock identifier for the product/container.

    qty:
        total number of new stock items to generate

    label_specification:
        label specification to use for the labels to be used for the
        new stock items

    dispense_to_new_container:
        if the old and new container are the same physical container,
        the old stock identifier matters and should be matched to the
        new label -- find the bottle with the old stock identifier
        and affix the new label

    Location is not changed here.

    """

    repack_identifier = models.CharField(
        max_length=36,
        unique=True,
        null=True,
        blank=True,
        help_text="Auto-generated by the EDC.",
    )

    repack_datetime = models.DateTimeField(default=get_utcnow)

    from_stock = models.ForeignKey(
        "edc_pharmacy.stock",
        on_delete=models.PROTECT,
        related_name="repack_requests",
        null=True,
        blank=False,
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

    label_specification = models.ForeignKey(
        LabelSpecificationProxy, on_delete=models.PROTECT, null=True, blank=False
    )

    processed = models.BooleanField(default=False)

    stock_count = models.IntegerField(null=True, blank=True)

    stock_identifiers = models.TextField(null=True, blank=True)
    confirmed_stock_identifiers = models.TextField(null=True, blank=True)
    unconfirmed_stock_identifiers = models.TextField(null=True, blank=True)

    objects = Manager()

    history = HistoricalRecords()

    def __str__(self):
        return self.repack_identifier

    def save(self, *args, **kwargs):
        if not self.repack_identifier:
            next_id = get_next_value(self._meta.label_lower)
            self.repack_identifier = f"{next_id:06d}"
        if not self.from_stock.confirmed:
            raise RepackRequestError(
                "Unconfirmed stock item. Only confirmed stock items may "
                "be used to repack. Perhaps catch this in the form"
            )
        super().save(*args, **kwargs)

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Repack request"
        verbose_name_plural = "Repack request"
