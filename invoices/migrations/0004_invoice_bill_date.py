# Generated by Django 2.2.12 on 2020-05-17 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invoices", "0003_auto_20200510_2040"),
    ]

    operations = [
        migrations.AddField(
            model_name="invoice",
            name="bill_date",
            field=models.DateField(editable=False, null=True),
        ),
    ]
