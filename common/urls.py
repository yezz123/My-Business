from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic import TemplateView

from common.views import SettingsView

urlpatterns = [
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("partners/", include("partners.urls", namespace="partners")),
    path("invoices/", include("invoices.urls", namespace="invoices")),
    path("servers/", include("servers.urls", namespace="servers")),
    path("settings/", SettingsView.as_view(), name="settings"),
    path(
        "",
        login_required(TemplateView.as_view(template_name="dashboard.html")),
        name="dashboard",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
