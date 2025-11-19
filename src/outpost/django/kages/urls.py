from django.urls import path

from . import views

app_name = "kages"

urlpatterns = [path("transfer/", views.TransferView.as_view(), name="transfer")]
