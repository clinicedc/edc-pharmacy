from bhp_base_model.tests.factories import BaseUuidModelFactory
from ph_dispenser.models import Dispensing
from ph_dispenser.choices import PACKING_UNITS


class DispensingFactory(BaseUuidModelFactory):
    FACTORY_FOR = Dispensing

    packing_amount = 25
    packing_unit = PACKING_UNITS[0][0]
    treatment = 'treatment'
    dose = 'dose'
