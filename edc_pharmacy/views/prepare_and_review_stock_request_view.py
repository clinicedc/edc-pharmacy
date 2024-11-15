from uuid import uuid4

import pandas as pd
from django.apps import apps as django_apps
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.views.generic import TemplateView
from edc_dashboard.view_mixins import EdcViewMixin
from edc_navbar import NavbarViewMixin
from edc_protocol.view_mixins import EdcProtocolViewMixin

from ..analytics import get_next_scheduled_visit_for_subjects_df
from ..models import StockRequest
from ..utils import bulk_create_stock_request_items, remove_subjects_where_stock_on_site


@method_decorator(login_required, name="dispatch")
class PrepareAndReviewStockRequestView(
    EdcViewMixin, NavbarViewMixin, EdcProtocolViewMixin, TemplateView
):
    template_name: str = "edc_pharmacy/stock/stock_request.html"
    navbar_name = settings.APP_NAME
    navbar_selected_item = "pharmacy"

    def get_context_data(self, **kwargs):
        stock_request = StockRequest.objects.get(pk=self.kwargs.get("stock_request"))
        df = get_next_scheduled_visit_for_subjects_df(stock_request)
        df = remove_subjects_where_stock_on_site(stock_request, df)

        df_instock = df[~df.code.isna()]
        df_instock = df_instock.reset_index(drop=True)
        df_instock = df_instock.sort_values(by=["subject_identifier"])

        df_nostock = df[df.code.isna()]
        df_nostock = df_nostock.reset_index(drop=True)
        df_nostock = df_nostock.loc[
            df_nostock.index.repeat(stock_request.containers_per_subject)
        ].reset_index(drop=True)
        df_nostock = df_nostock.sort_values(by=["subject_identifier"])
        df_nostock["code"] = df_nostock["code"].fillna("---")

        session_uuid = str(uuid4())
        nostock_dict = df_nostock.to_dict("list")
        self.request.session[session_uuid] = nostock_dict

        stock_request_items_exist = stock_request.stockrequestitem_set.all().exists()
        if stock_request_items_exist:
            messages.add_message(
                self.request,
                messages.ERROR,
                message=(
                    f"Stock request items already exist for "
                    f"{stock_request._meta.verbose_name} {stock_request.request_identifier}. "
                    "Create has been disabled."
                ),
            )
        kwargs.update(
            stock_request=stock_request,
            stock_request_items_exist=stock_request.stockrequestitem_set.all().exists(),
            source_model_name=self.model_cls._meta.verbose_name_plural,
            source_changelist_url=self.source_changelist_url,
            rows=len(df_nostock),
            subjects=df_nostock.subject_identifier.nunique(),
            nostock_table=format_html(
                df_nostock.to_html(
                    columns=[
                        "subject_identifier",
                        "next_visit_code",
                        "next_appt_datetime",
                    ],
                    index=True,
                    border=0,
                    classes="table table-striped",
                    table_id="my_table",
                )
            ),
            instock_table=format_html(
                df_instock.to_html(
                    columns=[
                        "subject_identifier",
                        "next_visit_code",
                        "next_appt_datetime",
                        "code",
                    ],
                    index=True,
                    border=0,
                    classes="table table-striped",
                    table_id="in_stock_table",
                )
            ),
            session_uuid=session_uuid,
        )
        return super().get_context_data(**kwargs)

    @property
    def source_changelist_url(self):
        return reverse("edc_pharmacy_admin:edc_pharmacy_stockrequest_changelist")

    @property
    def model_cls(self):
        return django_apps.get_model("edc_pharmacy.stocktransfer")

    def post(self, request, *args, **kwargs):
        session_uuid = request.POST.get("session_uuid")
        if not request.POST.get("cancel"):
            stock_request = StockRequest.objects.get(pk=request.POST.get("stock_request"))
            nostock_dict = request.session[session_uuid]
            if session_uuid:
                del request.session[session_uuid]
            df_nostock = pd.DataFrame(nostock_dict)
            created = bulk_create_stock_request_items(stock_request, df_nostock)
            messages.add_message(
                request,
                messages.SUCCESS,
                (
                    f"Successfully created {created} stock request items "
                    f"for request {stock_request.request_identifier}"
                ),
            )
            url = f"{self.source_changelist_url}?q={stock_request.request_identifier}"
        else:
            if session_uuid:
                del request.session[session_uuid]
            messages.add_message(
                request,
                messages.INFO,
                "Cancelled. No stock request items were created.",
            )
            url = f"{self.source_changelist_url}"
        return HttpResponseRedirect(url)