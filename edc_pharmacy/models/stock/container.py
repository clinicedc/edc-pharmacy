from django.db import models
from edc_model.models import BaseUuidModel

from .container_type import ContainerType
from .container_units import ContainerUnits


class Container(BaseUuidModel):

    name = models.CharField(max_length=50, unique=True, blank=True)

    container_type = models.ForeignKey(ContainerType, on_delete=models.PROTECT, null=True)

    units = models.ForeignKey(ContainerUnits, on_delete=models.PROTECT, null=True)

    qty = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    may_order_as = models.BooleanField(
        verbose_name="Container may be used for ordering", default=False
    )

    may_receive_as = models.BooleanField(
        verbose_name="Container may be used for receiving", default=False
    )

    may_request_as = models.BooleanField(
        verbose_name="Container may be used for stock request", default=False
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.container_type.name
            if self.qty > 1.0:
                self.name = f"{self.name} of {self.qty}"
            if self.may_request_as:
                self.name = f"{self.name} *"
                self.may_order_as = False
                self.may_receive_as = False
        super().save(*args, **kwargs)

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Stock: Container"
        verbose_name_plural = "Stock: Containers"
