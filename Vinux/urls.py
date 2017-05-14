
from django.conf.urls import  url
from . import controllerCellar

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^cellarView/$', controllerCellar.cellarView),
    url(r'^goneBottlesView/$', controllerCellar.goneBottlesView),
    url(r'^getCellar/$', controllerCellar.getCellar),
    url(r'^getGoneBottles/$', controllerCellar.getGoneBottles),
    url(r'^getDenominations/$', controllerCellar.getDenominations),
    url(r'^getProducers/$', controllerCellar.getProducers),
    url(r'^addBottle/$', controllerCellar.addBottle),
    url(r'^removeBottle/$', controllerCellar.removeBottle),
    url(r'^deleteBottle/$', controllerCellar.deleteBottle),
]

