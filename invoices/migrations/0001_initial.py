# Generated by Django 2.2.12 on 2020-05-10 00:00

from decimal import Decimal

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("partners", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Invoice",
            fields=[
                ("uid", models.AutoField(primary_key=True, serialize=False)),
                ("guid", models.CharField(max_length=12, unique=True)),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "Created: Waiting for billing"),
                            (1, "Sent: Waiting for payment"),
                            (2, "Rejected: Denied payment within 30 days"),
                            (3, "Paid: Received payment"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "hourly_rate",
                    models.DecimalField(
                        decimal_places=2,
                        default=Decimal("100.00"),
                        max_digits=6,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.00"))
                        ],
                    ),
                ),
                (
                    "partner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="invoices",
                        to="partners.Partner",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="InvoiceItem",
            fields=[
                ("uid", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=64)),
                (
                    "hours",
                    models.DecimalField(
                        decimal_places=1,
                        default=Decimal("0.0"),
                        max_digits=4,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.0"))
                        ],
                    ),
                ),
                (
                    "flat_amount",
                    models.DecimalField(
                        decimal_places=2,
                        default=Decimal("0.00"),
                        max_digits=6,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.00"))
                        ],
                    ),
                ),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "invoice",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="invoices.Invoice",
                    ),
                ),
            ],
        ),
    ]
