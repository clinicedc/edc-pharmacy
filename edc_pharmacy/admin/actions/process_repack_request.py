from __future__ import annotations

from celery import current_app
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from edc_utils.celery import run_task_sync_or_async

from ...tasks.process_repack_request import process_repack_request_queryset


@admin.action(description="Process repack request")
def process_repack_request_action(modeladmin, request, queryset):
    """Action to process repack request.

    Redirects to process_repack_request.

    If celery is running, will run through the entire queryset otherwise
    just the first instance in the queryset.

    """
    repack_request_pks = [obj.pk for obj in queryset]

    # if celery is not running, just keep the first pk
    i = current_app.control.inspect()
    if not i.active():
        repack_request_pks = repack_request_pks[:1]

    # run task / func and update or clear the task_id
    task = run_task_sync_or_async(
        process_repack_request_queryset, repack_request_pks=repack_request_pks
    )
    task_id = getattr(task, "id", None)
    queryset.update(task_id=task_id)

    # add messages for user
    messages.add_message(
        request,
        messages.SUCCESS,
        format_html(
            "Repack request submitted. <BR>Next, go to the ACTION menu below and "
            "(1)`Print labels`. Then (2) Label your stock containers with the printed labels. "
            "Once all stock is labelled, go to the ACTION menu below and "
            "(3) Select `Confirm repacked and labelled stock`. "
            f"Scan in the labels to CONFIRM the stock. ({task_id})"
        ),
    )
    if task_id:
        messages.add_message(
            request,
            messages.INFO,
            f"Task {task_id} is processing your repack requests.",
        )
    else:
        repack_request = queryset.first()
        messages.add_message(
            request,
            messages.INFO,
            (
                f"Processed only 1 of {queryset.count()} repack requests selected. "
                f"See {repack_request}."
            ),
        )
        messages.add_message(
            request, messages.ERROR, "Task workers not running. Contact data management."
        )

    # redirect to changelist
    url = reverse("edc_pharmacy_admin:edc_pharmacy_repackrequest_changelist")
    if queryset.count() == 1:
        repack_request = queryset.first()
        url = f"{url}?q={repack_request.from_stock.code}"
    return HttpResponseRedirect(url)
