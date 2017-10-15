from edc_pharma.constants import MILLIGRAM, CAPSULE, VIAL


class MedicationDefinition:
    def __init__(self, name=None, description=None, category=None,
                 unit=None, milligram=None, strength=None,
                 number_of_times_per_day=None, use_body_weight=None):
        self.name = name
        self.description = description
        self.category = category
        self.unit = unit
        self.milligram = milligram
        self.strength = strength
        self.number_of_times_per_day = number_of_times_per_day
        self.use_body_weight = use_body_weight


medications = {}
ambisome = MedicationDefinition(
    name='ambisome',
    description='Ambisome 10 mg/kg/day',
    category=VIAL,
    unit=MILLIGRAM,
    milligram=10,
    strength=50,
    number_of_times_per_day=4,
    use_body_weight=True)

medications.update({'ambisome': ambisome})

fluconazole = MedicationDefinition(
    name='fluconazole',
    description='Fluconazole 800mg/day',
    category=VIAL,
    unit=MILLIGRAM,
    milligram=1200,
    strength=500,
    number_of_times_per_day=4,
    use_body_weight=False)
medications.update({'fluconazole': fluconazole})

flucytosine = MedicationDefinition(
    name='flucytosine',
    description='Flucytosine 100mg/kg/day',
    category=CAPSULE,
    unit=MILLIGRAM,
    milligram=100,
    strength=500,
    number_of_times_per_day=4,
    use_body_weight=True)
medications.update({'flucytosine': flucytosine})

amphotericin = MedicationDefinition(
    name='amphotericin',
    description='Amphotericin B 1 mg/kg',
    category=CAPSULE,
    unit=MILLIGRAM,
    milligram=1,
    strength=50,
    number_of_times_per_day=4,
    use_body_weight=True)
medications.update({'amphotericin': amphotericin})
