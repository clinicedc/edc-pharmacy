# Generated by Django 6.0 on 2025-02-27 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_pharmacy", "0055_historicalreceiveitem_comment_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="historicallot",
            old_name="manufacture_date",
            new_name="manufactured_date",
        ),
        migrations.RenameField(
            model_name="lot",
            old_name="manufacture_date",
            new_name="manufactured_date",
        ),
        migrations.AddField(
            model_name="historicallot",
            name="comment",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="historicallot",
            name="country_of_origin",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="historicallot",
            name="manufactured_by",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="historicallot",
            name="processed_until_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="historicallot",
            name="reference",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="historicallot",
            name="storage_conditions",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="lot",
            name="comment",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="lot",
            name="country_of_origin",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="lot",
            name="manufactured_by",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="lot",
            name="processed_until_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="lot",
            name="reference",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="lot",
            name="storage_conditions",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
