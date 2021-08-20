from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    path("", views.ListView.as_view(), name="list"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("password/reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path(
        "password/reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset",
    ),
    path("create/", views.CreateView.as_view(), name="create"),
    path(
        "<int:uid>/password/change/",
        views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path("<int:uid>/", views.DetailView.as_view(), name="detail"),
    path("<int:uid>/edit/", views.EditView.as_view(), name="edit"),
    path("<int:uid>/delete/", views.DeleteView.as_view(), name="delete"),
    path("<int:uid>/type/", views.TypeView.as_view(), name="type"),
    path("shifts/create/", views.CreateShiftView.as_view(), name="shifts_create"),
    path("shifts/<int:uid>/edit/", views.EditShiftView.as_view(), name="shifts_edit"),
    path(
        "shifts/<int:uid>/delete/",
        views.DeleteShiftView.as_view(),
        name="shifts_delete",
    ),
]
