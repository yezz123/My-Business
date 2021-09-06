from django.urls import path

from invoices import views

app_name = "invoices"

urlpatterns = [
    path("", views.ListView.as_view(), name="list"),
    path("create/", views.CreateView.as_view(), name="create"),
    path("<int:uid>/", views.PDFView.as_view(), name="pdf"),
    path("<int:uid>/edit/", views.EditView.as_view(), name="edit"),
    path("<int:uid>/delete/", views.DeleteView.as_view(), name="delete"),
]
