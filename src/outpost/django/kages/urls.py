from django.conf.urls import url

from . import views

app_name = "kages"

urlpatterns = [url(r"^transfer/$", views.TransferView.as_view(), name="transfer")]
