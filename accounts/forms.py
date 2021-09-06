import datetime
import re
from configparser import ConfigParser
from smtplib import SMTPException

from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.mail.backends.smtp import EmailBackend
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode

from accounts.models import Account, Shift


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput(render_value=False)
    )

    def clean_email(self):
        return self.cleaned_data["email"].lower()

    def clean(self):
        if self._errors:
            return
        self.account = authenticate(
            email=self.cleaned_data["email"], password=self.cleaned_data["password"]
        )
        if self.account is None:
            raise forms.ValidationError(
                "The email and/or password you entered are incorrect."
            )
        return self.cleaned_data

    def login(self, request):
        if self.is_valid():
            login(request, self.account)
            return True
        return False


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="Email")

    def clean_email(self):
        try:
            self.account = Account.objects.get(email=self.cleaned_data["email"].lower())
        except Account.DoesNotExist:
            raise forms.ValidationError(
                "The email is not associated with any accounts."
            )
        return self.cleaned_data["email"].lower()

    def save(self, request):
        url = request.build_absolute_uri("/accounts/password/reset/")
        url += urlsafe_base64_encode(force_bytes(self.account.uid)) + "/"
        url += default_token_generator.make_token(self.account) + "/"

        html = render_to_string(
            "email.html",
            {
                "url": url,
                "message": "You requested a password reset.",
                "button": "Reset Password",
            },
        )
        text = strip_tags(html).replace("Reset Password", url)

        config = ConfigParser(interpolation=None)
        config.read(settings.CONFIG_FILE)

        backend = EmailBackend(
            host=config.get("email", "EMAIL_HOST"),
            port=config.getint("email", "EMAIL_PORT"),
            username=config.get("email", "EMAIL_USER"),
            password=config.get("email", "EMAIL_PASSWORD"),
            use_tls=config.getboolean("email", "EMAIL_USE_TLS"),
        )
        try:
            send_mail(
                subject="Reset Password | Business Tracker",
                message=text,
                html_message=html,
                from_email=config.get("email", "EMAIL_USER"),
                recipient_list=(self.cleaned_data["email"],),
                connection=backend,
            )
        except SMTPException:
            return False
        return True


class PasswordResetConfirmForm(forms.Form):
    new_password = forms.CharField(
        label="New Password", widget=forms.PasswordInput(render_value=False)
    )
    verify_new_password = forms.CharField(
        label="Verify New Password", widget=forms.PasswordInput(render_value=False)
    )

    def clean_new_password(self):
        if not re.match(settings.PASSWORD_REGEX, self.cleaned_data["new_password"]):
            raise forms.ValidationError(
                "The password needs to have at least 8 characters, a letter, and a number."
            )
        return self.cleaned_data["new_password"]

    def clean(self):
        if self._errors:
            return
        if (
            self.cleaned_data["new_password"]
            != self.cleaned_data["verify_new_password"]
        ):
            raise forms.ValidationError("The passwords do not match.")
        return self.cleaned_data

    def save(self, account):
        account.set_password(self.cleaned_data["new_password"])
        account.save()
        return account


class PasswordChangeForm(forms.Form):
    new_password = forms.CharField(
        label="New Password", widget=forms.PasswordInput(render_value=False)
    )
    verify_new_password = forms.CharField(
        label="Verify New Password", widget=forms.PasswordInput(render_value=False)
    )

    def clean_new_password(self):
        if not re.match(settings.PASSWORD_REGEX, self.cleaned_data["new_password"]):
            raise forms.ValidationError(
                "The password needs to have at least 8 characters, a letter, and a number."
            )
        return self.cleaned_data["new_password"]

    def clean(self):
        if self._errors:
            return
        if (
            self.cleaned_data["new_password"]
            != self.cleaned_data["verify_new_password"]
        ):
            raise forms.ValidationError("The passwords do not match.")
        return self.cleaned_data

    def save(self, account):
        account.set_password(self.cleaned_data["new_password"])
        account.save()
        return account


class AccountForm(forms.ModelForm):
    verify_email = forms.EmailField(label="Verify Email")

    class Meta:
        model = Account
        exclude = ("last_login", "password", "is_superuser")
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "address1": "Address Line 1",
            "address2": "Address Line 2",
            "state": "State / Region / Province",
            "zipcode": "ZIP / Postal Code",
        }

    def clean_email(self):
        return self.cleaned_data["email"].lower()

    def clean_verify_email(self):
        return self.cleaned_data["verify_email"].lower()

    def clean_first_name(self):
        if not re.match(settings.NAME_REGEX, self.cleaned_data["first_name"]):
            raise forms.ValidationError("Enter a valid first name.")
        return self.cleaned_data["first_name"]

    def clean_last_name(self):
        if not re.match(settings.NAME_REGEX, self.cleaned_data["last_name"]):
            raise forms.ValidationError("Enter a valid last name.")
        return self.cleaned_data["last_name"]

    def clean(self):
        self.cleaned_data = super().clean()
        if self._errors:
            return
        if self.cleaned_data["email"] != self.cleaned_data["verify_email"]:
            raise forms.ValidationError("The emails do not match.")
        return self.cleaned_data

    def save(self, request=None):
        account = super().save(commit=False)
        if not account._state.adding:
            account.save()
            return account

        account.is_superuser = False
        account.save()

        url = request.build_absolute_uri("/accounts/password/reset/")
        url += urlsafe_base64_encode(force_bytes(account.uid)) + "/"
        url += default_token_generator.make_token(account) + "/"

        html = render_to_string(
            "email.html",
            {
                "url": url,
                "message": f"{account.first_name}, activate your new account using the link below.",
                "button": "Activate Account",
            },
        )
        text = strip_tags(html).replace("Activate Account", url)

        config = ConfigParser(interpolation=None)
        config.read(settings.CONFIG_FILE)

        backend = EmailBackend(
            host=config.get("email", "EMAIL_HOST"),
            port=config.getint("email", "EMAIL_PORT"),
            username=config.get("email", "EMAIL_USER"),
            password=config.get("email", "EMAIL_PASSWORD"),
            use_tls=config.getboolean("email", "EMAIL_USE_TLS"),
        )
        try:
            send_mail(
                subject="Activate Account | Business Tracker",
                message=text,
                html_message=html,
                from_email=config.get("email", "EMAIL_USER"),
                recipient_list=(self.cleaned_data["email"],),
                connection=backend,
            )
            return account
        except SMTPException:
            return False


class ShiftForm(forms.ModelForm):
    duration = forms.CharField(
        max_length=5, help_text="Must be formatted as HH:MM (00:00 - 16:00)"
    )

    class Meta:
        model = Shift
        exclude = ("worker",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["project"].empty_label = ""
        if not self.initial.get("duration", None):
            self.initial["duration"] = "00:00"
        if not self.initial.get("date", None):
            self.initial["date"] = datetime.date.today()
        instance = getattr(self, "instance", None)
        if instance and instance.pk and self.initial["duration"]:
            hours = self.initial["duration"] // 3600
            minutes = self.initial["duration"] % 3600 // 60
            self.initial["duration"] = f"{hours:02d}:{minutes:02d}"

    def clean_duration(self):
        if len(self.cleaned_data["duration"]) != 5:
            raise forms.ValidationError("Enter a valid duration.")
        duration_str = self.cleaned_data["duration"].split(":")
        if not (duration_str[0].isdecimal() and duration_str[1].isdecimal()):
            raise forms.ValidationError("Enter a valid duration.")
        self.cleaned_data["duration"] = (
            int(duration_str[0]) * 3600 + int(duration_str[1]) * 60
        )
        if self.cleaned_data["duration"] not in range(60, 57601):
            raise forms.ValidationError("Enter a valid duration.")
        return self.cleaned_data["duration"]
