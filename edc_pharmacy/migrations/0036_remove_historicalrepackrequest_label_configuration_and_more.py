# Generated by Django 5.1.2 on 2024-11-09 22:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("edc_pharmacy", "0035_allocation_edc_pharmac_modifie_93b5ae_idx_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalrepackrequest",
            name="label_configuration",
        ),
        migrations.RemoveField(
            model_name="historicalstock",
            name="repack_request",
        ),
        migrations.RemoveField(
            model_name="repackrequest",
            name="label_configuration",
        ),
        migrations.RemoveField(
            model_name="stock",
            name="repack_request",
        ),
    ]
