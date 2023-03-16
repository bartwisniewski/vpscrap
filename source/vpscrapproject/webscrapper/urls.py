from django.urls import path
from django.urls import include
from django.contrib.auth.urls import urlpatterns
from webscrapper import views


urlpatterns = [
    path("scrap", views.Scrap.as_view(), name="scrap"),
    path("test", views.SendJsonView.as_view(), name="scrap-test"),
]
