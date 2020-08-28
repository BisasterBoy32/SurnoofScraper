from django.urls import path 
from . import views

urlpatterns = [
    path("", views.index, name="hame"),
    path("process/", views.process_data, name="proccess")
]
