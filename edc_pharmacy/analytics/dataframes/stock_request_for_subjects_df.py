import pandas as pd
from django.db.models import Q
from django_pandas.io import read_frame
from edc_appointment.analytics import get_appointment_df
from edc_consent.utils import get_consent_model_cls
from edc_sites.site import sites as site_sites

from ...models import Rx, StockRequest


def stock_request_for_subjects_df(stock_request_obj: StockRequest) -> pd.DataFrame:
    # get the next scheduled visit from appointment
    # subject_identifier, next_visit_code, next_appt_datetime
    df_appt = get_appointment_df(normalize=True, localize=True)
    df = (
        df_appt[
            (
                df_appt.next_appt_datetime
                > pd.Timestamp(stock_request_obj.request_datetime).to_datetime64()
            )
            & (df_appt.site_id == stock_request_obj.site_id)
        ]
        .groupby(by=["subject_identifier", "site_id"])
        .agg({"next_visit_code": "min", "next_appt_datetime": "min"})
    )
    df = df.reset_index()
    df = df.sort_values(by=["next_appt_datetime"])
    df = df.reset_index(drop=True)

    # merge with consent for gender
    df_consent = read_frame(
        get_consent_model_cls().objects.values("subject_identifier", "gender"),
        verbose=False,
    )
    df = df.merge(
        df_consent[["subject_identifier", "gender"]],
        on="subject_identifier",
        how="left",
        suffixes=("", "_y"),
    )
    df = df.reset_index(drop=True)

    # merge with prescription
    df_rx = read_frame(
        Rx.objects.values(
            "id", "registered_subject__subject_identifier", "rx_expiration_date", "rando_sid"
        ).filter(
            (
                Q(rx_expiration_date__gte=stock_request_obj.request_datetime.date())
                | Q(rx_expiration_date__isnull=True)
            ),
            medications__in=[stock_request_obj.formulation.medication],
        )
    )

    df_rx = df_rx.rename(
        columns={
            "registered_subject__subject_identifier": "subject_identifier",
            "id": "rx_id",
        }
    )
    df = df.merge(
        df_rx[["subject_identifier", "rx_id", "rando_sid"]],
        on="subject_identifier",
        how="left",
        suffixes=("", "_y"),
    )
    df = df[df.rx_id.notna()]
    df = df.reset_index(drop=True)

    df["site_name"] = df["site_id"].apply(lambda x: site_sites.get(x).name)
    return df
