import collections


Medication = collections.namedtuple(
    'Medication', 'name description unit instruction')

medications = {}
ambisome = Medication(
    name='ambisome',
    description='Ambisome 10 mg/kg/day',
    unit='10 mg/kg',
    instruction='NA')
medications.update({'ambisome': ambisome})
fluconazole = Medication(
    name='fluconazole',
    description='Fluconazole 1200mg/day',
    unit='1200mg',
    instruction='NA')
medications.update({'fluconazole': fluconazole})
flucytosine = Medication(
    name='flucytosine',
    description='Flucytosine 100mg',
    unit='100mg',
    instruction='NA')
medications.update({'flucytosine': flucytosine})

amphotericin = Medication(
    name='amphotericin',
    description='Amphotericin B 1 mg/kg',
    unit='1 mg/kg',
    instruction='NA')
medications.update({'amphotericin': amphotericin})
