import collections

from .constants import WEEKS
from .site_dispense_profiles import site_profiles

dispense_plan_control = collections.OrderedDict()
dispense_plan_control.update(
    {'schedule1': {
        'number_of_visits': 2,
        'duration': 2,
        'unit': WEEKS,
        'dispense_profile': {
            'enrollment': site_profiles.get(name='enrollment.control_arm'),
            'followup': site_profiles.get(name='followup.control_arm'),
        }
    }})
dispense_plan_control.update(
    {'schedule2': {
        'number_of_visits': 2,
        'duration': 8,
        'unit': WEEKS,
        'dispense_profile': {
            'enrollment': site_profiles.get(name='followup.control_arm'),
            'followup': site_profiles.get(name='followup.control_arm'),
        }
    }})

dispense_plan_singledose = collections.OrderedDict()
dispense_plan_singledose.update(
    {'schedule1': {
        'number_of_visits': 2,
        'duration': 2,
        'unit': WEEKS,
        'dispense_profile': {
            'enrollment': site_profiles.get(name='enrollment.single_dose'),
            'followup': site_profiles.get(name='followup.single_dose'),
        }
    }})
dispense_plan_singledose.update(
    {'schedule2': {
        'number_of_visits': 2,
        'duration': 8,
        'unit': WEEKS,
        'dispense_profile': {
            'enrollment': site_profiles.get(name='followup.single_dose'),
            'followup': site_profiles.get(name='followup.single_dose'),
        }
    }})
