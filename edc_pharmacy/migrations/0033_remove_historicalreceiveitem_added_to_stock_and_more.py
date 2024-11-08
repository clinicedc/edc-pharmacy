# Generated by Django 5.1.2 on 2024-11-08 01:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_pharmacy", "0032_container_qty_decimal_places"),
        ("edc_pylabels", "0006_delete_drawing"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalreceiveitem",
            name="added_to_stock",
        ),
        migrations.RemoveField(
            model_name="historicalrepackrequest",
            name="label_specification",
        ),
        migrations.RemoveField(
            model_name="receiveitem",
            name="added_to_stock",
        ),
        migrations.RemoveField(
            model_name="repackrequest",
            name="label_specification",
        ),
        migrations.AddField(
            model_name="historicalreceive",
            name="label_configuration",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="edc_pylabels.labelconfiguration",
            ),
        ),
        migrations.AddField(
            model_name="historicalrepackrequest",
            name="label_configuration",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="edc_pylabels.labelconfiguration",
            ),
        ),
        migrations.AddField(
            model_name="historicalstock",
            name="label_configuration",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="edc_pylabels.labelconfiguration",
            ),
        ),
        migrations.AddField(
            model_name="receive",
            name="label_configuration",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="edc_pylabels.labelconfiguration",
            ),
        ),
        migrations.AddField(
            model_name="repackrequest",
            name="label_configuration",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="edc_pylabels.labelconfiguration",
            ),
        ),
        migrations.AddField(
            model_name="stock",
            name="label_configuration",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="edc_pylabels.labelconfiguration",
            ),
        ),
    ]
