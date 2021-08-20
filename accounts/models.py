from django_countries.fields import CountryField
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from accounts.managers import AccountManager
from projects.models import Project


class Account(AbstractBaseUser):
    uid = models.AutoField(primary_key=True)
    email = models.EmailField(
        unique=True, error_messages={"unique": "This email is already in use."}
    )
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)

    address1 = models.CharField(
        max_length=48, blank=True, help_text="Street address, P.O. box"
    )
    address2 = models.CharField(
        max_length=32, blank=True, help_text="Apartment, suite, unit, building, floor"
    )
    city = models.CharField(max_length=32, blank=True)
    state = models.CharField(
        max_length=32, blank=True, help_text="Should use 2 letter "
    )
    zipcode = models.CharField(max_length=16, blank=True)
    country = CountryField(blank_label="", blank=True)

    is_superuser = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        ordering = ["first_name"]

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return self.first_name + " " + self.last_name


class Shift(models.Model):
    uid = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)
    duration = models.IntegerField()
    date = models.DateField()
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, related_name="shifts", null=True, blank=True
    )
    worker = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="shifts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        hours = self.duration // 3600
        minutes = self.duration % 3600 // 60
        return f"{hours:02d}:{minutes:02d}"

    class Meta:
        ordering = ["-date"]
