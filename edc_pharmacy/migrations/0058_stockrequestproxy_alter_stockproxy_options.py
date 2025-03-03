# Generated by Django 6.0 on 2025-03-04 16:19

import edc_pharmacy.models.stock.stock_request
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("edc_pharmacy", "0057_scanduplicates"),
    ]

    operations = [
        migrations.CreateModel(
            name="StockRequestProxy",
            fields=[],
            options={
                "verbose_name": "Stock Request",
                "verbose_name_plural": "Stock Requests",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("edc_pharmacy.stockrequest",),
            managers=[
                ("objects", edc_pharmacy.models.stock.stock_request.Manager()),
            ],
        ),
        migrations.AlterModelOptions(
            name="stockproxy",
            options={"verbose_name": "Stock", "verbose_name_plural": "Stock"},
        ),
    ]
