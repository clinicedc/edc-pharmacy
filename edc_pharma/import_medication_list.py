import collections
from edc_pharma.constants import MILLIGRAM, CAPSULE, VIAL


Medication = collections.namedtuple(
    'Medication', 'name description category unit volume amount number_of_times_per_day')

medications = {}
ambisome = Medication(
    name='ambisome',
    description='Ambisome 10 mg/kg/day',
    category=VIAL,
    unit=MILLIGRAM,
    volume=10,
    amount=500,
    number_of_times_per_day=4)
medications.update({'ambisome': ambisome})

fluconazole = Medication(
    name='fluconazole',
    description='Fluconazole 800mg/day',
    category=VIAL,
    unit=MILLIGRAM,
    volume=1200,
    amount=500,
    number_of_times_per_day=4)
medications.update({'fluconazole': fluconazole})

flucytosine = Medication(
    name='flucytosine',
    description='Flucytosine 100mg/kg/day',
    category=CAPSULE,
    unit=MILLIGRAM,
    volume=100,
    amount=500,
    number_of_times_per_day=4,)
medications.update({'flucytosine': flucytosine})

amphotericin = Medication(
    name='amphotericin',
    description='Amphotericin B 1 mg/kg',
    category=CAPSULE,
    unit=MILLIGRAM,
    volume=1,
    amount=50,
    number_of_times_per_day=4)
medications.update({'amphotericin': amphotericin})
