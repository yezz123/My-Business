from datetime import datetime, timedelta
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from common.mixins import AccessModelMixin, PermissionsRequiredMixin, NextPageMixin
from accounts.models import Account, Shift
from accounts.forms import *


class LoginView(View):
    def dispatch(self, request):
        self.next = request.GET.get("next", None)
        if not self.next or "://" in self.next or " " in self.next:
            self.next = "/"
        if request.user.is_authenticated:
            messages.add_message(request, messages.WARNING, "You are already logged in!")
            return HttpResponseRedirect(self.next)
        return super().dispatch(request)

    def get(self, request):
        form = LoginForm()
        return render(request=request, template_name="accounts/login.html", context={"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.login(request):
            messages.add_message(
                request, messages.SUCCESS, f"Welcome back, {request.user.first_name}! You have successfully logged in.",
            )
            return HttpResponseRedirect(self.next)
        return render(request=request, template_name="accounts/login.html", context={"form": form})


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.add_message(request, messages.SUCCESS, "You have successfully logged out.")
        else:
            messages.add_message(request, messages.WARNING, "You are already logged out!")
        return HttpResponseRedirect(reverse("accounts:login"))


class PasswordResetView(View):
    def dispatch(self, request):
        if request.user.is_authenticated:
            messages.add_message(
                request,
                messages.WARNING,
                "You have been redirected to change your password because you are logged in!",
            )
            return HttpResponseRedirect(reverse("accounts:password_change", args={request.user.uid}))
        return super().dispatch(request)

    def get(self, request):
        form = PasswordResetForm()
        return render(request=request, template_name="accounts/password/reset.html", context={"form": form})

    def post(self, request):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            if form.save(request=request):
                messages.add_message(request, messages.SUCCESS, "You have successfully requested a password reset.")
            else:
                messages.add_message(request, messages.ERROR, "The email settings are invalid.")
            return HttpResponseRedirect(reverse("accounts:login"))
        return render(request=request, template_name="accounts/password/reset.html", context={"form": form})


class PasswordResetConfirmView(View):
    def dispatch(self, request, uidb64, token):
        if request.user.is_authenticated:
            messages.add_message(
                request,
                messages.WARNING,
                "You have been redirected to change your password because you are logged in!",
            )
            return HttpResponseRedirect(reverse("accounts:password_change", args={request.user.uid}))
        try:
            self.account = Account.objects.get(uid=force_text(urlsafe_base64_decode(uidb64)))
            if default_token_generator.check_token(self.account, token):
                return super().dispatch(request)
            raise Account.DoesNotExist
        except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
            messages.add_message(request, messages.ERROR, "The request is invalid.")
            return HttpResponseRedirect(reverse("accounts:password_reset"))

    def get(self, request):
        form = PasswordResetConfirmForm()
        return render(request=request, template_name="accounts/password/set.html", context={"form": form})

    def post(self, request):
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            form.save(account=self.account)
            messages.add_message(request, messages.SUCCESS, "You have successfully set your password.")
            return HttpResponseRedirect(reverse("accounts:login"))
        return render(request=request, template_name="accounts/password/set.html", context={"form": form})


class PasswordChangeView(PermissionsRequiredMixin, AccessModelMixin, View):
    personal = True
    model = Account

    def get(self, request):
        form = PasswordChangeForm()
        return render(request=request, template_name="accounts/password/change.html", context={"form": form})

    def post(self, request):
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            form.save(self.account)
            messages.add_message(request, messages.SUCCESS, "You have successfully changed your password.")
            return HttpResponseRedirect(reverse("accounts:login"))
        return render(request=request, template_name="accounts/password/change.html", context={"form": form})


class ListView(PermissionsRequiredMixin, View):
    superuser = True

    def get(self, request):
        accounts = Account.objects.all()
        return render(request=request, template_name="accounts/list.html", context={"accounts": accounts})


class CreateView(PermissionsRequiredMixin, NextPageMixin, View):
    superuser = True

    def get(self, request):
        form = AccountForm()
        return render(request=request, template_name="accounts/create.html", context={"form": form})

    def post(self, request):
        form = AccountForm(request.POST)
        if form.is_valid():
            if form.save(request=request):
                messages.add_message(request, messages.SUCCESS, "The account has been successfully created.")
            else:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "The account has been created, but an activation email could not be sent.",
                )
            return HttpResponseRedirect(self.next)
        return render(request=request, template_name="accounts/create.html", context={"form": form})


class DetailView(PermissionsRequiredMixin, AccessModelMixin, View):
    personal = True
    superuser = True
    model = Account

    def get(self, request):
        return render(request=request, template_name="accounts/detail.html", context={"account": self.account})


class EditView(PermissionsRequiredMixin, NextPageMixin, AccessModelMixin, View):
    personal = True
    superuser = True
    model = Account

    def get(self, request):
        form = AccountForm(instance=self.account, initial={"verify_email": self.account.email})
        return render(request=request, template_name="accounts/edit.html", context={"form": form})

    def post(self, request):
        form = AccountForm(request.POST, instance=self.account)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "The account has been successfully edited.")
            return HttpResponseRedirect(self.next)
        return render(request=request, template_name="accounts/edit.html", context={"form": form})


class DeleteView(PermissionsRequiredMixin, NextPageMixin, AccessModelMixin, View):
    personal = True
    superuser = True
    model = Account

    def get(self, request):
        return render(request=request, template_name="accounts/delete.html")

    def post(self, request):
        self.account.delete()
        messages.add_message(request, messages.SUCCESS, "The account has been deleted.")
        return HttpResponseRedirect(self.next)


class TypeView(PermissionsRequiredMixin, NextPageMixin, AccessModelMixin, View):
    superuser = True
    model = Account

    def get(self, request):
        self.account.is_superuser = not self.account.is_superuser
        self.account.save()
        if self.account.is_superuser:
            messages.add_message(
                request, messages.SUCCESS, "The account type has been successfully changed to manager."
            )
        else:
            messages.add_message(
                request, messages.SUCCESS, "The account type has been successfully changed to developer."
            )
        return HttpResponseRedirect(self.next)


class CreateShiftView(PermissionsRequiredMixin, NextPageMixin, View):
    def get(self, request):
        form = ShiftForm()
        return render(request=request, template_name="accounts/shifts/create.html", context={"form": form})

    def post(self, request):
        form = ShiftForm(request.POST)
        if form.is_valid():
            shift = form.save(commit=False)
            shift.worker = request.user
            shift.save()
            messages.add_message(request, messages.SUCCESS, "The work shift has been successfully created.")
            form = ShiftForm()
        return render(request=request, template_name="accounts/shifts/create.html", context={"form": form})


class EditShiftView(PermissionsRequiredMixin, NextPageMixin, AccessModelMixin, View):
    personal = True
    model = Shift

    def get(self, request):
        form = ShiftForm(instance=self.shift)
        return render(request=request, template_name="accounts/shifts/edit.html", context={"form": form})

    def post(self, request):
        form = ShiftForm(request.POST, instance=self.shift)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "The work shift has been successfully edited.")
            return HttpResponseRedirect(self.next)
        return render(request=request, template_name="accounts/shifts/edit.html", context={"form": form})


class DeleteShiftView(PermissionsRequiredMixin, NextPageMixin, AccessModelMixin, View):
    personal = True
    model = Shift

    def get(self, request):
        return render(request=request, template_name="accounts/shifts/delete.html")

    def post(self, request):
        self.shift.delete()
        messages.add_message(request, messages.SUCCESS, "The work shift has been deleted.")
        return HttpResponseRedirect(self.next)
