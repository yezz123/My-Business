import re

from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseRedirect


class PermissionsRequiredMixin:
    superuser = False
    personal = False

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(
                request.get_full_path(), "/accounts/login/", "next"
            )
        if self.personal:
            if self.model.__name__.lower() == "account":
                if request.user.uid == kwargs.get("uid", -1):
                    return super().dispatch(request, *args, **kwargs)
            else:
                try:
                    models = getattr(request.user, self.model.__name__.lower() + "s")
                    if models.filter(uid=kwargs.get("uid", -1)).exists():
                        return super().dispatch(request, *args, **kwargs)
                except self.model.DoesNotExist:
                    pass
        if self.superuser and request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        if not self.personal and not self.superuser:
            return super().dispatch(request, *args, **kwargs)
        messages.add_message(
            request, messages.ERROR, "You don't have the required permissions."
        )
        return HttpResponseRedirect("/")


class AccessModelMixin:
    model = None

    def dispatch(self, request, uid, *args, **kwargs):
        try:
            setattr(
                self,
                re.sub(r"(?<!^)(?=[A-Z])", "_", self.model.__name__).lower(),
                self.model.objects.get(uid=uid),
            )
        except (TypeError, ValueError, OverflowError, self.model.DoesNotExist):
            messages.add_message(
                request,
                messages.ERROR,
                f"The {self.model.__name__.lower()} doesn't exist.",
            )
            return HttpResponseRedirect("/")
        return super().dispatch(request, *args, **kwargs)


class NextPageMixin:
    def dispatch(self, request, *args, **kwargs):
        setattr(self, "next", request.GET.get("next"))
        if (
            not getattr(self, "next")
            or "://" in getattr(self, "next")
            or " " in getattr(self, "next")
        ):
            setattr(self, "next", "/")
        return super().dispatch(request, *args, **kwargs)
