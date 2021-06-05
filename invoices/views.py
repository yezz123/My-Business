from datetime import date
from django.views import View
from django.conf import settings
from django.shortcuts import render, reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from common.mixins import AccessModelMixin, PermissionsRequiredMixin, NextPageMixin
from invoices.models import Invoice, Item
from invoices.forms import InvoiceForm, ItemForm
from invoices.utils import generate_id, generate_pdf
from django.forms import inlineformset_factory


class ListView(PermissionsRequiredMixin, View):
    def get(self, request):
        invoices = Invoice.objects.all()
        paid_btn = {"active": "", "pressed": "", "href": "?hide=1", "text": "Hide"}
        void_btn = {"active": "", "pressed": "", "href": "?hide=2", "text": "Hide"}

        if request.GET.get("hide", None) == "1":
            invoices = invoices.exclude(status=3)
            paid_btn = {"active": "active", "pressed": "true", "href": "", "text": "Show"}
            void_btn["href"] = "?hide=3"
        elif request.GET.get("hide", None) == "2":
            invoices = invoices.exclude(status=4)
            void_btn = {"active": "active", "pressed": "true", "href": "", "text": "Show"}
            paid_btn["href"] = "?hide=3"
        elif request.GET.get("hide", None) == "3":
            invoices = invoices.exclude(status=3)
            invoices = invoices.exclude(status=4)
            paid_btn = {"active": "active", "pressed": "true", "href": "?hide=2", "text": "Show"}
            void_btn = {"active": "active", "pressed": "true", "href": "?hide=1", "text": "Show"}

        return render(
            request=request,
            template_name="invoices/list.html",
            context={"invoices": invoices, "paid_btn": paid_btn, "void_btn": void_btn},
        )


class CreateView(PermissionsRequiredMixin, NextPageMixin, View):
    superuser = True

    def get(self, request):
        form = InvoiceForm()
        return render(request=request, template_name="invoices/create.html", context={"form": form})

    def post(self, request):
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.invoice_id = generate_id(form.cleaned_data["partner"])
            invoice.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, "The invoice has been successfully created.")
            return HttpResponseRedirect(self.next)
        return render(request=request, template_name="invoices/create.html", context={"form": form})


class PDFView(PermissionsRequiredMixin, AccessModelMixin, View):
    model = Invoice

    def get(self, request):
        pdf = generate_pdf(self.invoice)
        if not pdf:
            messages.add_message(request, messages.ERROR, "The invoice template is invalid.")
            return HttpResponseRedirect(reverse("invoices:list"))
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="{self.invoice.invoice_id}.pdf"'
        return response


class EditView(PermissionsRequiredMixin, AccessModelMixin, NextPageMixin, View):
    superuser = True
    model = Invoice

    def get(self, request):
        form = InvoiceForm(instance=self.invoice)
        if self.invoice.items.count():
            extra = 0
        else:
            extra = 1

        if self.invoice.status > 0:
            return render(request=request, template_name="invoices/edit.html", context={"form": form})

        ItemsFormSet = inlineformset_factory(Invoice, Item, fields="__all__", extra=extra)
        formset = ItemsFormSet(instance=self.invoice)
        return render(request=request, template_name="invoices/edit.html", context={"form": form, "formset": formset})

    def post(self, request):
        form = InvoiceForm(request.POST, instance=self.invoice)

        if self.invoice.status > 0:
            if form.is_valid():
                invoice = form.save()
                if invoice.status == 1 and not invoice.bill_date:
                    invoice.bill_date = date.today()
                    invoice.save()
                messages.add_message(request, messages.SUCCESS, "The invoice has been successfully edited.")
                return HttpResponseRedirect(self.next)
            return render(request=request, template_name="invoices/edit.html", context={"form": form})

        ItemsFormSet = inlineformset_factory(Invoice, Item, fields="__all__", extra=0)
        formset = ItemsFormSet(request.POST, instance=self.invoice)
        if form.is_valid() and formset.is_valid():
            invoice = form.save()
            if invoice.status == 1 and not invoice.bill_date:
                invoice.bill_date = date.today()
                invoice.save()
            formset.save()
            messages.add_message(request, messages.SUCCESS, "The invoice has been successfully edited.")
            return HttpResponseRedirect(self.next)
        return render(request=request, template_name="invoices/edit.html", context={"form": form, "formset": formset})


class DeleteView(PermissionsRequiredMixin, AccessModelMixin, NextPageMixin, View):
    superuser = True
    model = Invoice

    def get(self, request):
        if self.invoice.status > 0:
            messages.add_message(
                request, messages.ERROR, "The invoice is not deletable anymore. If needed, mark it as obsolete"
            )
            return HttpResponseRedirect(self.next)
        return render(request=request, template_name="invoices/delete.html")

    def post(self, request):
        if self.invoice.status > 0:
            messages.add_message(request, messages.ERROR, "The invoice is not deletable anymore.")
            return HttpResponseRedirect(self.next)
        self.invoice.delete()
        messages.add_message(request, messages.SUCCESS, "The invoice has been deleted.")
        return HttpResponseRedirect(self.next)
