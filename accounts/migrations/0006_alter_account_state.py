# Generated by Django 3.2.6 on 2021-08-20 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_auto_20200723_1859"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="state",
            field=models.CharField(
                blank=True, help_text="Should use 2 letter ", max_length=32
            ),
        ),
    ]