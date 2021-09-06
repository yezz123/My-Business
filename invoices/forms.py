from django import forms

from invoices.models import STATUS, Invoice, Item


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = "__all__"
        labels = {"invoice_id": "Invoice ID"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["partner"].empty_label = ""
        self.fields["status"] = forms.ChoiceField(choices=STATUS)
        self.instance = getattr(self, "instance", None)
        if self.instance and self.instance.pk:
            self.fields["invoice_id"].disabled = True
            self.fields["partner"].disabled = True
        else:
            self.fields["status"].disabled = True
            self.fields["status"].required = False
            self.fields.pop("invoice_id")

    def clean(self):
        self.cleaned_data = super().clean()
        if self.instance.pk:
            if int(self.cleaned_data["status"]) == 2 and self.instance.status != 2:
                raise forms.ValidationError(
                    "The status cannot be manually set to OVERDUE. Business Tracker automatically sets an invoice as OVERDUE 30 days after it was billed."
                )
            if int(self.cleaned_data["status"]) < self.instance.status:
                raise forms.ValidationError(
                    "The status must advance or stay the same ("
                    + STATUS[self.instance.status][1]
                    + ")."
                )
            if (
                self.instance.status < 1
                and int(self.cleaned_data["status"]) > 1
                and int(self.cleaned_data["status"]) < 4
            ):
                raise forms.ValidationError(
                    "The status cannot be advanced to OVERDUE or PAID because the invoice has not been billed yet."
                )
            if self.instance.status == 3 and int(self.cleaned_data["status"]) == 4:
                raise forms.ValidationError(
                    "The status cannot be advanced to VOID because the invoice has been paid. retry or done!"
                )


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"
