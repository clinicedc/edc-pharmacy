# Generated by Django 5.1.2 on 2024-11-21 03:43

import edc_utils.date
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_pharmacy", "0050_remove_stocktransferconfirmation2_location_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="historicalstocktransferconfirmationitem",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Stock Transfer Confirmation Item",
                "verbose_name_plural": "historical Stock Transfer Confirmation Items",
            },
        ),
        migrations.AlterModelOptions(
            name="stocktransferconfirmationitem",
            options={
                "default_manager_name": "objects",
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "verbose_name": "Stock Transfer Confirmation Item",
                "verbose_name_plural": "Stock Transfer Confirmation Items",
            },
        ),
        migrations.RenameField(
            model_name="historicalstocktransferconfirmation",
            old_name="confirmation_identifier",
            new_name="transfer_confirmation_identifier",
        ),
        migrations.RenameField(
            model_name="historicalstocktransferconfirmationitem",
            old_name="confirmation_item_datetime",
            new_name="transfer_confirmation_item_datetime",
        ),
        migrations.RenameField(
            model_name="historicalstocktransferconfirmationitem",
            old_name="confirmation_item_identifier",
            new_name="transfer_confirmation_item_identifier",
        ),
        migrations.RenameField(
            model_name="stocktransferconfirmation",
            old_name="confirmation_identifier",
            new_name="transfer_confirmation_identifier",
        ),
        migrations.RenameField(
            model_name="stocktransferconfirmationitem",
            old_name="confirmation_item_datetime",
            new_name="transfer_confirmation_item_datetime",
        ),
        migrations.RenameField(
            model_name="stocktransferconfirmationitem",
            old_name="confirmation_item_identifier",
            new_name="transfer_confirmation_item_identifier",
        ),
        migrations.RemoveField(
            model_name="historicalstocktransferconfirmation",
            name="confirmation_datetime",
        ),
        migrations.RemoveField(
            model_name="stocktransferconfirmation",
            name="confirmation_datetime",
        ),
        migrations.AddField(
            model_name="historicalstocktransferconfirmation",
            name="transfer_confirmation_datetime",
            field=models.DateTimeField(default=edc_utils.date.get_utcnow),
        ),
        migrations.AddField(
            model_name="stocktransferconfirmation",
            name="transfer_confirmation_datetime",
            field=models.DateTimeField(default=edc_utils.date.get_utcnow),
        ),
    ]
