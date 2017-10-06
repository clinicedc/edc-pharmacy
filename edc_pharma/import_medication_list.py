import collections


Medication = collections.namedtuple(
    'Medication', 'name description weight instruction')

medications = {}
ambisome = Medication(
    name='ambisome',
    description='Ambisome 10 mg/kg/day',
    weight='10 mg/kg',
    instruction='NA')
medications.update({'ambisome': ambisome})
fluconazole = Medication(
    name='fluconazole',
    description='Fluconazole 1200mg/day',
    weight='1200mg',
    instruction='NA')
medications.update({'fluconazole': fluconazole})
flucytosine = Medication(
    name='flucytosine',
    description='Flucytosine 100mg',
    weight='100mg',
    instruction='NA')
medications.update({'flucytosine': flucytosine})

amphotericin = Medication(
    name='amphotericin',
    description='Amphotericin B 1 mg/kg',
    weight='1 mg/kg',
    instruction='NA')
medications.update({'amphotericin': amphotericin})
