# Generated by Django 5.1.2 on 2024-11-12 15:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_pharmacy", "0052_allocation_assignment"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalstockrequestitem",
            name="assignment",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="edc_pharmacy.assignment",
            ),
        ),
        migrations.AddField(
            model_name="stockrequestitem",
            name="assignment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="edc_pharmacy.assignment",
            ),
        ),
        migrations.AlterField(
            model_name="allocation",
            name="assignment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="edc_pharmacy.assignment",
            ),
        ),
        migrations.AlterField(
            model_name="allocation",
            name="registered_subject",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="edc_pharmacy.registeredsubjectproxy",
                verbose_name="Allocated to",
            ),
        ),
        migrations.AlterField(
            model_name="allocation",
            name="stock_request_item",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="edc_pharmacy.stockrequestitem",
                verbose_name="Requested",
            ),
        ),
    ]
