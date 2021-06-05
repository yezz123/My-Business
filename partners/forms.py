import re
from django import forms
from django.conf import settings
from partners.models import Partner


class PartnerForm(forms.ModelForm):
    contact_phone = forms.RegexField(
        label="Contact Phone Number",
        regex=r"^\+?[0-9]+$",
        max_length=16,
        help_text="Must have only digits and an optional country code prefixed with a plus sign",
    )

    class Meta:
        model = Partner
        fields = "__all__"
        labels = {
            "partner_id": "Partner ID",
            "company": "Company / Organization / University",
            "contact_name": "Contact Name",
            "contact_email": "Contact Email",
            "address1": "Address Line 1",
            "address2": "Address Line 2",
            "state": "State / Region / Province",
            "zipcode": "ZIP / Postal Code",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)
        if instance and instance.pk:
            self.fields["partner_id"].disabled = True
        else:
            self.fields["partner_id"].required = False
            self.fields["partner_id"].help_text = "Must be exactly 3 characters long"

    def clean_partner_id(self):
        length = len(self.cleaned_data["partner_id"])
        if length != 0 and length != 3:
            raise forms.ValidationError("Enter a valid Partner ID.")
        return self.cleaned_data["partner_id"]

    def clean_contact_name(self):
        if not re.match(settings.NAME_REGEX, self.cleaned_data["contact_name"]):
            raise forms.ValidationError("Enter a valid name.")
        return self.cleaned_data["contact_name"]

    def clean_contact_email(self):
        return self.cleaned_data["contact_email"].lower()
