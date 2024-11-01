from django.db import models
from edc_constants.constants import NEW
from edc_model.models import BaseUuidModel, HistoricalRecords
from sequences import get_next_value

from ...choices import ORDER_CHOICES
from .container import Container
from .order import Order
from .product import Product


class Manager(models.Manager):
    use_in_migrations = True


class OrderItem(BaseUuidModel):

    order_item_identifier = models.CharField(max_length=36, unique=True, null=True, blank=True)

    order = models.ForeignKey(Order, on_delete=models.PROTECT)

    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    container = models.ForeignKey(Container, on_delete=models.PROTECT)

    unit_qty = models.DecimalField(null=True, blank=False, decimal_places=2, max_digits=10)

    container_qty = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    container_qty_received = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    status = models.CharField(
        max_length=25, choices=ORDER_CHOICES, default=NEW, help_text="Updates in the signal"
    )

    objects = Manager()

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.order_item_identifier}:{self.product.name} | {self.container.name}"

    def save(self, *args, **kwargs):
        if not self.order_item_identifier:
            self.order_item_identifier = f"{get_next_value(self._meta.label_lower):06d}"
        if self.container.container_qty > 1:
            self.container_qty = self.unit_qty * self.container.container_qty
        else:
            self.container_qty = self.unit_qty
        super().save(*args, **kwargs)

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Stock: Order item"
        verbose_name_plural = "Stock: Order items"
