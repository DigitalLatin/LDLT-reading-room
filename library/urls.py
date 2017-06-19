from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^texts/([^/]+)$', views.edition),
    url(r'^texts/([^/]+)/([0-9a-zA-Z]+)$', views.edition),
]
