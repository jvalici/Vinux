
from django.conf.urls import  url
from . import controllerCellar

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    url(r'^homeView/$', controllerCellar.homeView),
]

