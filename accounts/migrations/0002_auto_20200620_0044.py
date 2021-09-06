# Generated by Django 2.2.12 on 2020-06-20 00:44

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=datetime.datetime(1970, 1, 1, 0, 0)
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="account",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
