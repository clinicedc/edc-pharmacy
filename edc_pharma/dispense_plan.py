import collections

from .constants import WEEKS
from .print_profile import site_profiles

dispense_plans = collections.OrderedDict()
dispense_plan_control = collections.OrderedDict()
dispense_plan_control.update(
    {'schedule1': {
        'number_of_visits': 2,
        'duration': 2,
        'unit': WEEKS,
        'description': 'Enrollment Schedule 1',
        'dispense_profile': {
            'enrollment': site_profiles.get(name='enrollment.control'),
            'followup': site_profiles.get(name='followup.control'),
        }
    }})
dispense_plan_control.update(
    {'schedule2': {
        'number_of_visits': 2,
        'duration': 8,
        'unit': WEEKS,
        'description': 'Follow Up Schedule 1',
        'dispense_profile': {
            'enrollment': site_profiles.get(name='followup.control'),
            'followup': site_profiles.get(name='followup.control'),
        }
    }})

dispense_plan_singledose = collections.OrderedDict()
dispense_plan_singledose.update(
    {'schedule1': {
        'number_of_visits': 2,
        'duration': 2,
        'unit': WEEKS,
        'description': 'Enrollment Schedule 2',
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
        'description': 'Follow Up Schedule 2',
        'dispense_profile': {
            'enrollment': site_profiles.get(name='followup.single_dose'),
            'followup': site_profiles.get(name='followup.single_dose'),
        }
    }})

dispense_plans.update({'control': dispense_plan_control})
dispense_plans.update({'single_dose': dispense_plan_singledose})
