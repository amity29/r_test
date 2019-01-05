from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^datadump/', views.datadump),
    url(r'^flight_decision/', views.flight_decision),
    url(r'^flightpricing/', views.flightpricing),
    url(r'^test/', views.conncheck),
]

# http://127.0.0.1:8000/flight_decision/?sc=KWI&dest=CAI&date=08-01-2019
