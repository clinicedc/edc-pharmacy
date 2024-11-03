from django.db import models
from django.db.models import PROTECT
from edc_constants.constants import CLOSED, OPEN
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_sites.model_mixins import SiteModelMixin
from edc_utils import get_utcnow
from sequences import get_next_value

from ...exceptions import InvalidContainer
from ..medication import Formulation
from ..storage import Location
from .container import Container


class Manager(models.Manager):
    use_in_migrations = True


class Request(SiteModelMixin, BaseUuidModel):
    """A model to represent a stock request for subject stock.

    A request originates from, or is linked to, the research site.
    """

    request_identifier = models.CharField(max_length=36, unique=True, null=True, blank=True)

    request_datetime = models.DateTimeField(default=get_utcnow)

    name = models.CharField(max_length=50, unique=True)

    formulation = models.ForeignKey(Formulation, on_delete=models.PROTECT)

    container = models.ForeignKey(Container, on_delete=models.PROTECT, null=True, blank=False)

    default_qty = models.PositiveSmallIntegerField(
        verbose_name="Default number of containers per item", default=1
    )

    location = models.ForeignKey(Location, verbose_name="Requested from", on_delete=PROTECT)

    item_count = models.IntegerField(
        verbose_name="Actual containers in this request",
        default=0,
        help_text="Matches the number of StockRequestItems",
    )

    labels = models.TextField(
        verbose_name="Labels",
        null=True,
        blank=True,
        help_text=(
            "A cell to capture and confirm printed/scanned labels related to this "
            "Stock request. See StockRequestItem."
        ),
    )

    status = models.CharField(
        max_length=25,
        choices=((OPEN, OPEN.title()), (CLOSED, CLOSED.title())),
        default=OPEN,
    )

    objects = Manager()

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if not self.request_identifier:
            self.request_identifier = get_next_value(self._meta.label_lower)
        if not self.container.may_request_as:
            raise InvalidContainer(
                "Invalid stock.container. Must be a `subject-specific` container. "
                "Perhaps catch this in the form."
            )
        super().save(*args, **kwargs)

    class Meta(SiteModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Stock: Request"
        verbose_name_plural = "Stock: Request"
