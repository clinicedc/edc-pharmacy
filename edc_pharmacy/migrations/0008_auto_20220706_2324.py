# Generated by Django 3.2.13 on 2022-07-06 20:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("edc_pharmacy", "0007_auto_20220704_1841"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalrxrefill",
            name="frequency",
        ),
        migrations.RemoveField(
            model_name="historicalrxrefill",
            name="frequency_units",
        ),
        migrations.RemoveField(
            model_name="rxrefill",
            name="frequency",
        ),
        migrations.RemoveField(
            model_name="rxrefill",
            name="frequency_units",
        ),
        migrations.AddField(
            model_name="historicalrxrefill",
            name="round_dose",
            field=models.IntegerField(
                default=0, help_text="Rounds the dose. e.g. 7.3->7.0, 7.5->8.0"
            ),
        ),
        migrations.AddField(
            model_name="historicalrxrefill",
            name="roundup_dose",
            field=models.BooleanField(
                default=False, help_text="Rounds UP the dose. e.g. 7.3->8.0, 7.5->8.0"
            ),
        ),
        migrations.AddField(
            model_name="rxrefill",
            name="round_dose",
            field=models.IntegerField(
                default=0, help_text="Rounds the dose. e.g. 7.3->7.0, 7.5->8.0"
            ),
        ),
        migrations.AddField(
            model_name="rxrefill",
            name="roundup_dose",
            field=models.BooleanField(
                default=False, help_text="Rounds UP the dose. e.g. 7.3->8.0, 7.5->8.0"
            ),
        ),
        migrations.AlterField(
            model_name="historicalrxrefill",
            name="roundup_divisible_by",
            field=models.IntegerField(
                default=0,
                help_text="Rounds up the total. For example, 32 would round 112 pills to 128 pills",
            ),
        ),
        migrations.AlterField(
            model_name="historicalrxrefill",
            name="total",
            field=models.DecimalField(
                blank=True,
                decimal_places=4,
                help_text="Total to be dispensed. Leave blank to auto-calculate",
                max_digits=10,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="historicalrxrefill",
            name="weight_in_kgs",
            field=models.DecimalField(
                blank=True,
                decimal_places=1,
                help_text="Defaults to 1.0",
                max_digits=6,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="rxrefill",
            name="roundup_divisible_by",
            field=models.IntegerField(
                default=0,
                help_text="Rounds up the total. For example, 32 would round 112 pills to 128 pills",
            ),
        ),
        migrations.AlterField(
            model_name="rxrefill",
            name="total",
            field=models.DecimalField(
                blank=True,
                decimal_places=4,
                help_text="Total to be dispensed. Leave blank to auto-calculate",
                max_digits=10,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="rxrefill",
            name="weight_in_kgs",
            field=models.DecimalField(
                blank=True,
                decimal_places=1,
                help_text="Defaults to 1.0",
                max_digits=6,
                null=True,
            ),
        ),
    ]
