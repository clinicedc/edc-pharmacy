from edc_auth.site_auths import site_auths
from edc_auth.utils import remove_default_model_permissions_from_edc_permissions

from .auth_objects import (
    PHARMACIST_ROLE,
    PHARMACY,
    PHARMACY_AUDITOR_ROLE,
    PHARMACY_PRESCRIBER,
    PHARMACY_PRESCRIBER_ROLE,
    PHARMACY_VIEW,
    SITE_PHARMACIST_ROLE,
    pharmacy_codenames,
    pharmacy_navbar_codenames,
    pharmacy_navbar_tuples,
    prescriber_codenames,
)

site_auths.add_post_update_func(
    "edc_pharmacy", remove_default_model_permissions_from_edc_permissions
)
site_auths.add_custom_permissions_tuples(
    model="edc_pharmacy.edcpermissions", codename_tuples=pharmacy_navbar_tuples
)

site_auths.add_group(
    *pharmacy_codenames, *pharmacy_navbar_codenames, name=PHARMACY_VIEW, view_only=True
)
site_auths.add_group(
    *pharmacy_codenames, *pharmacy_navbar_codenames, name=PHARMACY, no_delete=False
)
site_auths.add_group(
    *prescriber_codenames, *pharmacy_navbar_codenames, name=PHARMACY_PRESCRIBER, no_delete=True
)

site_auths.add_role(PHARMACY, name=PHARMACIST_ROLE)
site_auths.add_role(PHARMACY, name=SITE_PHARMACIST_ROLE)
site_auths.add_role(PHARMACY_PRESCRIBER, name=PHARMACY_PRESCRIBER_ROLE)
site_auths.add_role(PHARMACY_VIEW, name=PHARMACY_AUDITOR_ROLE)
