from decimal import Decimal
from django.db import models
from django_countries.fields import CountryField


class Partner(models.Model):
    uid = models.AutoField(primary_key=True)
    partner_id = models.CharField(
        max_length=3,
        unique=True,
        error_messages={"unique": "This Partner ID is already in use."},
    )
    company = models.CharField(max_length=64, unique=True)
    contact_name = models.CharField(max_length=64)
    contact_email = models.EmailField()
    contact_phone = models.CharField(
        max_length=16,
        blank=True,
        help_text="Must have only digits and an optional country code prefixed with a plus sign",
    )
    address1 = models.CharField(max_length=48, help_text="Street address, P.O. box")
    address2 = models.CharField(
        max_length=32, blank=True, help_text="Apartment, suite, unit, building, floor"
    )
    city = models.CharField(max_length=32)
    state = models.CharField(
        max_length=32, help_text="Should use 2 letter abbreviations for U.S. states"
    )
    zipcode = models.CharField(max_length=16)
    country = CountryField(blank_label="")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["company"]

    def __str__(self):
        return self.company

    def get_pretty_contact_phone(self):
        if len(self.contact_phone) == 10:
            return f"({self.contact_phone[:3]}) {self.contact_phone[3:6]}-{self.contact_phone[6:10]}"
        elif len(self.contact_phone) in [12, 13] and self.contact_phone[0] == "+":
            return f"{self.contact_phone[:-10]} ({self.contact_phone[-10:-7]}) {self.contact_phone[-7:-4]}-{self.contact_phone[-4:]}"
        else:
            return self.contact_phone

    def get_address1(self):
        address = self.address1
        if self.address2:
            address += ", " + self.address2
        return address

    def get_address2(self):
        address = self.city
        address += ", " + self.state
        address += " " + self.zipcode
        return address

    def get_statistics(self):
        statistics = {
            "non_void_invoices_count": self.invoices.exclude(status=4).count()
        }

        # The total amount of money this partner has been billed for
        statistics["total_billed"] = Decimal("0.00")
        for invoice in self.invoices.exclude(status=4).exclude(status=0):
            statistics["total_billed"] += invoice.get_total()

        return statistics

    def get_last_invoice(self):
        return self.invoices.exclude(status=4).exclude(status=0).last()
