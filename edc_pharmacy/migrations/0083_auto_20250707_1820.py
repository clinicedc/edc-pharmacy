# Generated by Django 5.2.3 on 2025-07-07 15:20
from django.core.exceptions import ObjectDoesNotExist
from django.db import migrations
from tqdm import tqdm

from edc_pharmacy.models import Confirmation, Stock


def update_confirm(apps, schema_editor):
    qs = Stock.objects.filter(confirmed=True)
    total = qs.count()
    for stock in tqdm(qs, total=total):
        try:
            Confirmation.objects.get(stock=stock)
        except ObjectDoesNotExist:
            obj = Confirmation(
                stock=stock,
                confirmed_by=stock.confirmed_by,
                confirmed_datetime=stock.confirmed_datetime,
            )
            obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ("edc_pharmacy", "0082_alter_confirmation_managers_remove_confirmation_site_and_more"),
    ]

    operations = [migrations.RunPython(update_confirm)]
