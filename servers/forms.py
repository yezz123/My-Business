from django import forms

from servers.models import Server


class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = "__all__"
        labels = {"uid": "Linode ID", "root_password": "Root Password"}
        widgets = {
            "services": forms.Textarea(
                attrs={
                    "placeholder": "Follow the format: Service (Product) - URL\n"
                    "E.g. GDGSNF (LibreOrganize) - gdgsnf.github.io"
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        if getattr(self, "instance") and self.instance.pk:
            self.fields["uid"].disabled = True
