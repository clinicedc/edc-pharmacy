# Generated by Django 5.1.2 on 2024-11-18 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("edc_pharmacy", "0041_alter_dispenseitem_dispense_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicaldispensinghistory",
            name="history_user",
        ),
        migrations.RemoveField(
            model_name="historicaldispensinghistory",
            name="rx_refill",
        ),
        migrations.RemoveField(
            model_name="historicalreturnhistory",
            name="history_user",
        ),
        migrations.RemoveField(
            model_name="historicalreturnhistory",
            name="rx_refill",
        ),
        migrations.AlterUniqueTogether(
            name="returnhistory",
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name="returnhistory",
            name="rx_refill",
        ),
        migrations.DeleteModel(
            name="DispensingHistory",
        ),
        migrations.DeleteModel(
            name="HistoricalDispensingHistory",
        ),
        migrations.DeleteModel(
            name="HistoricalReturnHistory",
        ),
        migrations.DeleteModel(
            name="ReturnHistory",
        ),
    ]
