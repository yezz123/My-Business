# Generated by Django 2.2.12 on 2020-05-10 01:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("invoices", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="invoiceitem", old_name="hours", new_name="worked_hours",
        ),
    ]
