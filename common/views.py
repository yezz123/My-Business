from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.views import View

from common.forms import SettingsForm
from common.mixins import PermissionsRequiredMixin


class SettingsView(PermissionsRequiredMixin, View):
    superuser = True

    def get(self, request):
        form = SettingsForm()
        return render(
            request=request, template_name="settings.html", context={"form": form}
        )

    def post(self, request):
        form = SettingsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            new_template = request.FILES.get("invoice_template", None)
            if new_template:
                with open(settings.TEMPLATE_FILE, "wb+") as destination:
                    for chunk in new_template.chunks():
                        destination.write(chunk)
            messages.add_message(
                request, messages.SUCCESS, "The settings have been sucessfully saved.",
            )

            form = SettingsForm()
        return render(
            request=request, template_name="settings.html", context={"form": form}
        )
