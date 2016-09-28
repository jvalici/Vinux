
from django.conf.urls import  url
from . import controllerCellar, views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()




urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^test/$', controllerCellar.getTestJson),
]

