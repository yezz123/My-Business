from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.html import mark_safe
from accounts.models import Account
from partners.models import Partner


STATUS = (
    (0, "DRAFT: Waiting for billing"),
    (1, "BILLED: Waiting for payment"),
    (2, "OVERDUE: Waiting for payment (over 30 days)"),
    (3, "PAID: Received payment"),
    (4, "VOID: Cancelled invoice"),
)
STATUS_EXTRA = (
    ("primary", "<i class='fas fa-edit fa-fw'></i> DRAFT", "Waiting for billing"),
    ("warning", "<i class='fas fa-paper-plane fa-fw'></i> BILLED", "Waiting for payment"),
    ("careful", "<i class='fas fa-exclamation-triangle fa-fw'></i> OVERDUE", "Waiting for payment (over 30 days)"),
    ("success", "<i class='fas fa-check fa-fw'></i> PAID", "Received payment"),
    ("danger", "<i class='fas fa-ban fa-fw'></i> VOID", "Cancelled invoice"),
)


class Invoice(models.Model):
    uid = models.AutoField(primary_key=True)
    invoice_id = models.CharField(max_length=12, unique=True)
    partner = models.ForeignKey(Partner, related_name="invoices", on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(default=0)
    bill_date = models.DateField(editable=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.invoice_id

    def get_html_status(self):
        return mark_safe(
            f'<span class="badge badge-{STATUS_EXTRA[self.status][0]} font-weight-normal">{STATUS_EXTRA[self.status][1]}</span> <span>{STATUS_EXTRA[self.status][2]}</span>'
        )

    def get_total(self):
        total = Decimal("0.00")
        for item in self.items.all():
            total += item.amount
        return total


class Item(models.Model):
    uid = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, related_name="items", on_delete=models.CASCADE)
    description = models.CharField(max_length=96)
    hours = models.DecimalField(
        max_digits=3, decimal_places=1, blank=True, null=True, validators=[MinValueValidator(Decimal("0.1"))]
    )
    rate = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(Decimal("0.1"))]
    )
    amount = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal("0.1"))])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
