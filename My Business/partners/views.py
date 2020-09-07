from django.views import View
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from common.mixins import AccessModelMixin, PermissionsRequiredMixin, NextPageMixin
from partners.models import Partner
from partners.forms import PartnerForm
from partners.utils import generate_id


class ListView(PermissionsRequiredMixin, View):
    def get(self, request):
        partners = Partner.objects.all()
        return render(request=request, template_name="partners/list.html", context={"partners": partners})


class CreateView(PermissionsRequiredMixin, NextPageMixin, View):
    superuser = True

    def get(self, request):
        form = PartnerForm()
        return render(request=request, template_name="partners/create.html", context={"form": form})

    def post(self, request):
        form = PartnerForm(request.POST)
        if form.is_valid():
            partner = form.save(commit=False)
            partner.partner_id = generate_id(form.cleaned_data["company"])
            partner.save()
            messages.add_message(request, messages.SUCCESS, "The partner has been successfully created.")
            return HttpResponseRedirect(self.next)
        return render(request=request, template_name="partners/create.html", context={"form": form})


class DetailView(PermissionsRequiredMixin, AccessModelMixin, View):
    model = Partner

    def get(self, request):
        return render(request=request, template_name="partners/detail.html", context={"partner": self.partner})


class EditView(PermissionsRequiredMixin, AccessModelMixin, NextPageMixin, View):
    superuser = True
    model = Partner

    def get(self, request):
        form = PartnerForm(instance=self.partner)
        return render(request=request, template_name="partners/edit.html", context={"form": form})

    def post(self, request):
        form = PartnerForm(request.POST, instance=self.partner)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "The partner has been successfully edited.")
            return HttpResponseRedirect(self.next)
        return render(request=request, template_name="partners/edit.html", context={"form": form})


class DeleteView(PermissionsRequiredMixin, AccessModelMixin, NextPageMixin, View):
    superuser = True
    model = Partner

    def get(self, request):
        return render(request=request, template_name="partners/delete.html")

    def post(self, request):
        self.partner.delete()
        messages.add_message(request, messages.SUCCESS, "The partner has been deleted.")
        return HttpResponseRedirect(self.next)
