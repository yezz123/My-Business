# Generated by Django 2.2.12 on 2020-07-02 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("partners", "0005_auto_20200620_0044"),
    ]

    operations = [
        migrations.AlterField(
            model_name="partner",
            name="address1",
            field=models.CharField(help_text="Street address, P.O. box", max_length=48),
        ),
        migrations.AlterField(
            model_name="partner",
            name="address2",
            field=models.CharField(
                blank=True,
                help_text="Apartment, suite, unit, building, floor",
                max_length=32,
            ),
        ),
        migrations.AlterField(
            model_name="partner",
            name="partner_id",
            field=models.CharField(
                error_messages={"unique": "This Partner ID is already in use."},
                max_length=3,
                unique=True,
            ),
        ),
    ]
