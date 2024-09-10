# Generated by Django 5.1 on 2024-09-09 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_action_item", "0037_remove_actionitem_reference_model_and_more"),
        ("edc_pharmacy", "0022_alter_historicalproduct_site_alter_historicalrx_site_and_more"),
        ("sites", "0002_alter_domain_unique"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="rx",
            name="edc_pharmac_modifie_986021_idx",
        ),
        migrations.RemoveIndex(
            model_name="rx",
            name="edc_pharmac_user_mo_b9ac53_idx",
        ),
        migrations.AddIndex(
            model_name="rx",
            index=models.Index(fields=["rando_sid"], name="edc_pharmac_rando_s_0bcc84_idx"),
        ),
    ]
