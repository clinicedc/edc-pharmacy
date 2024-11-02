from django.db import models
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel

from .stock_transfer import StockTransfer


class StockTransferItems(NonUniqueSubjectIdentifierFieldMixin, BaseUuidModel):
    """Model for items in a stock transfer request.

    List of items is generated based on participant study status
    and existing on site stock.

    May also need site to site transfer and
    Manual transfer -- one-off request in case of emergency
    """

    stock_transfer_request = models.ForeignKey(StockTransfer, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Stock Transfer: Items"
        verbose_name_plural = "Stock Transfer: Items"