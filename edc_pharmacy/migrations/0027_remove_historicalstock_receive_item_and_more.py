# Generated by Django 5.1.2 on 2024-11-07 00:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_pharmacy", "0026_remove_container_may_repackage_as_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalstock",
            name="receive_item",
        ),
        migrations.RemoveField(
            model_name="stock",
            name="receive_item",
        ),
        migrations.AddField(
            model_name="historicalreceive",
            name="confirmed_stock_identifiers",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="historicalreceive",
            name="stock_identifiers",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="historicalreceive",
            name="unconfirmed_stock_identifiers",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="receive",
            name="confirmed_stock_identifiers",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="receive",
            name="stock_identifiers",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="receive",
            name="stock_items",
            field=models.ManyToManyField(to="edc_pharmacy.stock"),
        ),
        migrations.AddField(
            model_name="receive",
            name="unconfirmed_stock_identifiers",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="historicalrepackrequest",
            name="container",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                limit_choices_to={"may_repack_as": True},
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="edc_pharmacy.container",
            ),
        ),
        migrations.AlterField(
            model_name="repackrequest",
            name="container",
            field=models.ForeignKey(
                limit_choices_to={"may_repack_as": True},
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="edc_pharmacy.container",
            ),
        ),
    ]
