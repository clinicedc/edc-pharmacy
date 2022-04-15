from uuid import uuid4

from django.db import models
from django.db.models import PROTECT
from edc_model import models as edc_models
from edc_sites.models import SiteModelMixin

from .formulation import Formulation
from .list_models import Container
from .medication_lot import MedicationLot


class Manager(models.Manager):

    use_in_migrations = True

    # def get_by_natural_key(self, container, count_per_container, *args):
    #     Medication.objects.get(*args)
    #     return self.get(name, strength, units, formulation)


class MedicationProduct(SiteModelMixin, edc_models.BaseUuidModel):

    product_identifier = models.CharField(max_length=36, default=uuid4, unique=True)

    name = models.CharField(max_length=250, unique=True, editable=False)

    container = models.ForeignKey(Container, on_delete=PROTECT)

    count_per_container = models.DecimalField(
        verbose_name="Items per container", max_digits=6, decimal_places=1
    )

    formulation = models.ForeignKey(Formulation, on_delete=PROTECT)

    lot_no = models.ForeignKey(MedicationLot, on_delete=PROTECT)

    objects = Manager()

    history = edc_models.HistoricalRecords()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = (
            f"{self.formulation.medication.display_name} {self.formulation.strength}{self.formulation.units}. "
            f"LOT#: {self.lot_no.lot_no}. {self.container} of {self.count_per_container}"
        )
        super().save(*args, **kwargs)

    class Meta(SiteModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Medication product"
        verbose_name_plural = "Medication products"