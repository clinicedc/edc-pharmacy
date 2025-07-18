# Generated by Django 5.2.3 on 2025-07-08 12:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_pharmacy", "0084_confirmationatsiteitem_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="confirmationatsite",
            options={
                "default_manager_name": "objects",
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "verbose_name": "Stock Confirmation at Site ",
                "verbose_name_plural": "Stock Confirmations at Site",
            },
        ),
        migrations.AlterModelOptions(
            name="confirmationatsiteitem",
            options={
                "default_manager_name": "objects",
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "verbose_name": "Stock Confirmation at Site Item",
                "verbose_name_plural": "Stock Confirmation at Site Items",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalconfirmationatsite",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Stock Confirmation at Site ",
                "verbose_name_plural": "historical Stock Confirmations at Site",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalconfirmationatsiteitem",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Stock Confirmation at Site Item",
                "verbose_name_plural": "historical Stock Confirmation at Site Items",
            },
        ),
        migrations.RenameField(
            model_name="confirmationatsiteitem",
            old_name="stock_transfer_confirmation",
            new_name="confirmation_at_site",
        ),
        migrations.RenameField(
            model_name="historicalconfirmationatsiteitem",
            old_name="stock_transfer_confirmation",
            new_name="confirmation_at_site",
        ),
        migrations.RenameIndex(
            model_name="confirmationatsite",
            new_name="edc_pharmac_modifie_0b23c2_idx",
            old_name="edc_pharmac_modifie_88e9fc_idx",
        ),
        migrations.RenameIndex(
            model_name="confirmationatsite",
            new_name="edc_pharmac_user_mo_2f1be6_idx",
            old_name="edc_pharmac_user_mo_9c1939_idx",
        ),
        migrations.RenameIndex(
            model_name="confirmationatsiteitem",
            new_name="edc_pharmac_modifie_d7c6b9_idx",
            old_name="edc_pharmac_modifie_84ddbd_idx",
        ),
        migrations.RenameIndex(
            model_name="confirmationatsiteitem",
            new_name="edc_pharmac_user_mo_0acc89_idx",
            old_name="edc_pharmac_user_mo_956b50_idx",
        ),
        migrations.RemoveField(
            model_name="historicalstock",
            name="confirmed_at_site",
        ),
        migrations.RemoveField(
            model_name="historicalstock",
            name="dispense",
        ),
        migrations.RemoveField(
            model_name="historicalstock",
            name="transferred",
        ),
        migrations.RemoveField(
            model_name="stock",
            name="confirmed_at_site",
        ),
        migrations.RemoveField(
            model_name="stock",
            name="dispense",
        ),
        migrations.RemoveField(
            model_name="stock",
            name="transferred",
        ),
        migrations.AlterField(
            model_name="historicalstoragebinitem",
            name="stock",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                limit_choices_to={
                    "confirmationatsiteitem__isnull": False,
                    "dispenseitem__isnull": True,
                },
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="edc_pharmacy.stock",
            ),
        ),
        migrations.AlterField(
            model_name="storagebinitem",
            name="stock",
            field=models.ForeignKey(
                limit_choices_to={
                    "confirmationatsiteitem__isnull": False,
                    "dispenseitem__isnull": True,
                },
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="edc_pharmacy.stock",
            ),
        ),
    ]
