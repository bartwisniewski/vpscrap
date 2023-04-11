from django.urls import path
from django.urls import include
from django.contrib.auth.urls import urlpatterns
from webscrapper import views


urlpatterns = [
    path("scrap/", views.Scrap.as_view(), name="scrap"),
    path("check/<str:task_id>/", views.Check.as_view(), name="check"),
    path("result/<str:task_id>/", views.Result.as_view(), name="result"),
    path("test", views.SendJsonView.as_view(), name="scrap-test"),
]
