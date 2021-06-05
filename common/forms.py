from configparser import ConfigParser
from django import forms
from django.conf import settings


class SettingsForm(forms.Form):
    invoice_template = forms.FileField(
        required=False, label="Invoice Template", help_text="Can be left empty to keep the current template"
    )
    email_host = forms.CharField(required=False, label="Email Host", help_text="E.g. mail.business.org")
    email_port = forms.IntegerField(label="Email Port")
    email_user = forms.CharField(
        required=False, label="Email User", help_text="E.g. do-not-reply@business.org"
    )
    email_password = forms.CharField(required=False, label="Email Password")
    email_use_tls = forms.BooleanField(required=False, label="Use TLS for Email")
    weekly_hours = forms.IntegerField(
        label="Weekly Required Hours", help_text="The amount of hours someone should work per week"
    )
    overdue_days = forms.IntegerField(
        label="Overdue Days",
        help_text="The amount of days after which an invoice is marked as overdue (Use 0 for never)",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Read the config.ini file
        self.config = ConfigParser(interpolation=None)
        self.config.read(settings.CONFIG_FILE)

        # Set initial values from the config file
        self.initial["email_host"] = self.config.get("email", "EMAIL_HOST")
        self.initial["email_port"] = self.config.getint("email", "EMAIL_PORT")
        self.initial["email_user"] = self.config.get("email", "EMAIL_USER")
        self.initial["email_password"] = self.config.get("email", "EMAIL_PASSWORD")
        self.initial["email_use_tls"] = self.config.getboolean("email", "EMAIL_USE_TLS")
        self.initial["weekly_hours"] = self.config.getint("accounts", "WEEKLY_HOURS")
        self.initial["overdue_days"] = self.config.getint("invoices", "OVERDUE_DAYS")

    def clean_email_port(self):
        if not self.cleaned_data["email_port"] in range(0, 65535):
            raise forms.ValidationError("Enter an integer between 0 and 65535.")
        return self.cleaned_data["email_port"]

    def clean_weekly_hours(self):
        if self.cleaned_data["weekly_hours"] < 0:
            raise forms.ValidationError("Enter a positive integer.")
        return self.cleaned_data["weekly_hours"]

    def clean_overdue_days(self):
        if self.cleaned_data["overdue_days"] < 0:
            raise forms.ValidationError("Enter a positive integer.")
        return self.cleaned_data["overdue_days"]

    def save(self):
        self.config.set("email", "EMAIL_HOST", self.cleaned_data["email_host"])
        self.config.set("email", "EMAIL_PORT", str(self.cleaned_data["email_port"]))
        self.config.set("email", "EMAIL_USER", self.cleaned_data["email_user"])
        self.config.set("email", "EMAIL_PASSWORD", self.cleaned_data["email_password"])
        self.config.set("email", "EMAIL_USE_TLS", str(self.cleaned_data["email_use_tls"]))
        self.config.set("accounts", "WEEKLY_HOURS", str(self.cleaned_data["weekly_hours"]))
        self.config.set("invoices", "OVERDUE_DAYS", str(self.cleaned_data["overdue_days"]))

        with open(settings.CONFIG_FILE, "w") as f:
            self.config.write(f, space_around_delimiters=False)
