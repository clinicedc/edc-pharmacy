from __future__ import annotations

import ast

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from edc_dashboard.view_mixins import EdcViewMixin
from edc_navbar import NavbarViewMixin
from edc_protocol.view_mixins import EdcProtocolViewMixin

from ..exceptions import AllocationError
from ..models import Assignment, Stock, StockRequest, StockRequestItem
from ..utils import allocate_stock


@method_decorator(login_required, name="dispatch")
class AllocateToSubjectView(EdcViewMixin, NavbarViewMixin, EdcProtocolViewMixin, TemplateView):
    model_pks: list[str] | None = None
    template_name: str = "edc_pharmacy/stock/allocate_to_subject.html"
    navbar_name = settings.APP_NAME
    navbar_selected_item = "pharmacy"

    def get_context_data(self, **kwargs):
        kwargs.update(
            stock_request=self.stock_request,
            assignment=self.selected_assignment,
            stock_request_changelist_url=self.stock_request_changelist_url,
            subject_identifiers=self.get_next_subject_identifiers(12),
            subject_identifiers_count=self.subject_identifiers.count(),
            assignments=Assignment.objects.all().order_by("name"),
        )
        return super().get_context_data(**kwargs)

    @property
    def subject_identifiers(self):
        """Returns a queryset of unallocated stock request
        items for the given assignment.
        """
        return (
            StockRequestItem.objects.values_list(
                "registered_subject__subject_identifier", flat=True
            )
            .filter(
                stock_request=self.stock_request,
                allocation__isnull=True,
                assignment=self.selected_assignment,
            )
            .order_by("registered_subject__subject_identifier")
        )

    @property
    def stock_request(self):
        stock_request_id = self.kwargs.get("stock_request")
        try:
            stock_request = StockRequest.objects.get(id=stock_request_id)
        except ObjectDoesNotExist:
            stock_request = None
            messages.add_message(self.request, messages.ERROR, "Invalid stock request.")
        return stock_request

    @property
    def selected_assignment(self):
        assignment_id = self.kwargs.get("assignment")
        try:
            assignment = Assignment.objects.get(id=assignment_id)
        except ObjectDoesNotExist:
            assignment = None
        return assignment

    def get_next_subject_identifiers(self, count: int | None = None) -> list[str]:
        if self.selected_assignment:
            subject_identifiers = self.subject_identifiers
            if count:
                return [s for s in subject_identifiers[:count]]
            return [s for s in subject_identifiers]
        return []

    @property
    def stock_request_changelist_url(self) -> str:
        if self.stock_request:
            url = reverse("edc_pharmacy_admin:edc_pharmacy_stockrequest_changelist")
            url = f"{url}?q={self.stock_request.request_identifier}"
            return url
        return "/"

    def validate_containers(self, stock_codes: list[str], stock_request: StockRequest) -> bool:
        if stock_codes and Stock.objects.filter(
            code__in=stock_codes, container=stock_request.container
        ).count() != len(stock_codes):
            messages.add_message(
                self.request,
                messages.ERROR,
                (
                    f"Container mismatch for request. Expected `{stock_request.container}` "
                    f"only. See Stock request {stock_request.request_identifier} "
                ),
            )
            return False
        return True

    @staticmethod
    def get_assignment(assignment_id) -> Assignment | None:
        try:
            assignment = Assignment.objects.get(id=assignment_id)
        except ObjectDoesNotExist:
            assignment = None
        return assignment

    def stock_already_allocated(self, stock_codes: list[str]) -> bool:
        if (
            stock_codes
            and Stock.objects.filter(code__in=stock_codes, allocation__isnull=False).exists()
        ):
            assigned_codes = []
            for stock in Stock.objects.filter(code__in=stock_codes):
                if stock.allocation:
                    assigned_codes.append(stock.code)
            messages.add_message(
                self.request,
                messages.ERROR,
                f"Stock already allocated. Got {','.join(assigned_codes)}.",
            )
            return False
        return True

    def post(self, request, *args, **kwargs):
        stock_codes = request.POST.getlist("codes") if request.POST.get("codes") else None
        subject_identifiers = request.POST.get("subject_identifiers")
        assignment_id = request.POST.get("assignment")
        subject_identifiers = ast.literal_eval(subject_identifiers)
        stock_request = StockRequest.objects.get(id=kwargs.get("stock_request"))
        if self.validate_containers(stock_codes, stock_request):
            assignment = self.get_assignment(assignment_id)
            subject_identifiers = [] if self.stock_already_allocated() else subject_identifiers
            if subject_identifiers and assignment:
                allocation_data = dict(zip(stock_codes, subject_identifiers))
                try:
                    allocated, not_allocated = allocate_stock(
                        stock_request, allocation_data, allocated_by=request.user.username
                    )
                except AllocationError as e:
                    messages.add_message(request, messages.ERROR, str(e))
                else:
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        f"Allocated {allocated} stock records. Skipped {not_allocated}.",
                    )
                if self.get_next_subject_identifiers():
                    url = reverse(
                        "edc_pharmacy:allocate_url",
                        kwargs={
                            "stock_request": stock_request.id,
                            "assignment": assignment.id,
                        },
                    )
                    return HttpResponseRedirect(url)
                return HttpResponseRedirect(self.stock_request_changelist_url)
            url = reverse(
                "edc_pharmacy:allocate_url",
                kwargs={
                    "stock_request": stock_request.id,
                    "assignment": getattr(assignment, "id", None),
                },
            )
            return HttpResponseRedirect(url)
        return HttpResponseRedirect(self.stock_request_changelist_url)