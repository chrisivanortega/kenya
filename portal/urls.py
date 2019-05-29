from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admins$', views.admins, name='index'),
    url(r'^registro$', views.registro, name='index'),
    url(r'^registros$', views.registros, name='index'),
    url(r'^login$', views.login, name='index'),
    url(r'^logout$', views.logout, name='index'),
    
]