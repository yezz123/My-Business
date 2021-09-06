# Generated by Django 2.2.12 on 2020-05-09 22:07

from django.db import migrations, models

import accounts.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Account",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("uid", models.AutoField(primary_key=True, serialize=False)),
                (
                    "email",
                    models.EmailField(
                        error_messages={"unique": "This email is already in use."},
                        max_length=254,
                        unique=True,
                    ),
                ),
                ("first_name", models.CharField(max_length=32)),
                ("last_name", models.CharField(max_length=32)),
                ("is_superuser", models.BooleanField()),
            ],
            options={"abstract": False,},
            managers=[("objects", accounts.managers.AccountManager()),],
        ),
    ]
