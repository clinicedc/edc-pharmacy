from uuid import uuid4

from django.contrib import admin, messages
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext

from edc_pharmacy.models import Stock


@admin.action(description="Print labels")
def print_labels(modeladmin, request, queryset):
    selected = request.POST.getlist(ACTION_CHECKBOX_NAME)
    if len(selected) > 0:
        session_uuid = str(uuid4())
        request.session[session_uuid] = selected
        url = reverse(
            "edc_pharmacy:print_labels_url",
            kwargs={"session_uuid": session_uuid, "model": "stock"},
        )
        return HttpResponseRedirect(url)
    return None


@admin.action(description="Print labels")
def print_labels_from_repack_request(modeladmin, request, queryset):
    if queryset.count() > 1 or queryset.count() == 0:
        messages.add_message(
            request,
            messages.ERROR,
            gettext("Select one and only one item"),
        )
    else:
        session_uuid = str(uuid4())
        stock_qs = Stock.objects.values_list("pk", flat=True).filter(
            repack_request=queryset.first()
        )
        if stock_qs.exists():
            request.session[session_uuid] = [o for o in stock_qs]
            url = reverse(
                "edc_pharmacy:print_labels_url",
                kwargs={"session_uuid": session_uuid, "model": "stock"},
            )
            return HttpResponseRedirect(url)
    return None
