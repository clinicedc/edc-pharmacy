import collections


Medication = collections.namedtuple(
    'Medication', 'name description weight instruction times_per_day'
    ' total_number_of_tablets')

medications = {}
ambisome = Medication(
    name='ambisome',
    description='Ambisome 10 mg/kg/day',
    weight='10 mg/kg',
    instruction='NA',
    times_per_day=None,
    total_number_of_tablets=None)
medications.update({'ambisome': ambisome})
fluconazole = Medication(
    name='fluconazole',
    description='Fluconazole 1200mg/day',
    weight='1200mg',
    instruction='NA',
    times_per_day=None,
    total_number_of_tablets=None)
medications.update({'fluconazole': fluconazole})
flucytosine = Medication(
    name='flucytosine',
    description='Flucytosine 100mg',
    weight='100mg',
    instruction='NA',
    times_per_day=None,
    total_number_of_tablets=None)
medications.update({'flucytosine': flucytosine})

amphotericin = Medication(
    name='amphotericin',
    description='Amphotericin B 1 mg/kg',
    weight='1 mg/kg',
    instruction='NA',
    times_per_day=None,
    total_number_of_tablets=None)
medications.update({'amphotericin': amphotericin})
