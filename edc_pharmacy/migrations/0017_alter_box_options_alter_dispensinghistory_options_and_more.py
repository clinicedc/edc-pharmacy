# Generated by Django 4.2.1 on 2023-07-05 02:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("edc_pharmacy", "0016_auto_20220929_1742"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="box",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Box",
                "verbose_name_plural": "Boxes",
            },
        ),
        migrations.AlterModelOptions(
            name="dispensinghistory",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Dispensing history",
                "verbose_name_plural": "Dispensing history",
            },
        ),
        migrations.AlterModelOptions(
            name="dosageguideline",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Dosage Guideline",
                "verbose_name_plural": "Dosage Guidelines",
            },
        ),
        migrations.AlterModelOptions(
            name="formulation",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Formulation",
                "verbose_name_plural": "Formulations",
            },
        ),
        migrations.AlterModelOptions(
            name="genericcontainer",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Item",
                "verbose_name_plural": "Items",
            },
        ),
        migrations.AlterModelOptions(
            name="labels",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Label",
                "verbose_name_plural": "Labels",
            },
        ),
        migrations.AlterModelOptions(
            name="location",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Location",
                "verbose_name_plural": "Locations",
            },
        ),
        migrations.AlterModelOptions(
            name="medication",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Medication",
                "verbose_name_plural": "Medications",
            },
        ),
        migrations.AlterModelOptions(
            name="medicationlot",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Medication lot",
                "verbose_name_plural": "Medication lots",
            },
        ),
        migrations.AlterModelOptions(
            name="order",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Medication order",
                "verbose_name_plural": "Medication orders",
            },
        ),
        migrations.AlterModelOptions(
            name="pillbottle",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Pill Bottle",
                "verbose_name_plural": "Pill Bottles",
            },
        ),
        migrations.AlterModelOptions(
            name="product",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Medication product",
                "verbose_name_plural": "Medication products",
            },
        ),
        migrations.AlterModelOptions(
            name="returnhistory",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Return history",
                "verbose_name_plural": "Return history",
            },
        ),
        migrations.AlterModelOptions(
            name="room",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Room",
                "verbose_name_plural": "Rooms",
            },
        ),
        migrations.AlterModelOptions(
            name="rx",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Prescription",
                "verbose_name_plural": "Prescriptions",
            },
        ),
        migrations.AlterModelOptions(
            name="rxrefill",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "RX refill",
                "verbose_name_plural": "RX refills",
            },
        ),
        migrations.AlterModelOptions(
            name="shelf",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Shelf",
                "verbose_name_plural": "Shelves",
            },
        ),
        migrations.AlterModelOptions(
            name="stock",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Medication stock",
                "verbose_name_plural": "Medication stock",
            },
        ),
        migrations.AlterModelOptions(
            name="stockcreatelabels",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Medication stock: Create labels",
                "verbose_name_plural": "Medication stock: Create labels",
            },
        ),
        migrations.AlterModelOptions(
            name="stockreceiving",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Medication stock: Receiving",
                "verbose_name_plural": "Medication stock: Receiving",
            },
        ),
        migrations.AlterModelOptions(
            name="subjectpillbottle",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Subject Pill Bottle",
                "verbose_name_plural": "Subject Pill Bottles",
            },
        ),
    ]
