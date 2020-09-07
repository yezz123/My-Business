from django.urls import path
from partners import views

app_name = "partners"

urlpatterns = [
    path("", views.ListView.as_view(), name="list"),
    path("create/", views.CreateView.as_view(), name="create"),
    path("<int:uid>/", views.DetailView.as_view(), name="detail"),
    path("<int:uid>/edit/", views.EditView.as_view(), name="edit"),
    path("<int:uid>/delete/", views.DeleteView.as_view(), name="delete"),
]
