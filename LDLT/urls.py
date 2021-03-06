"""LDLT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
    
    Old rule: url(r'^$', RedirectView.as_view(url='/library/', permanent=True)),
"""
from django.conf.urls import include, url
from django.contrib import admin
#from django.views.generic import RedirectView
from library import views

urlpatterns = [
        #url(r'^$', RedirectView.as_view(url='/library/', permanent=True)),
        #url(r'^$', views.splash, name='splash', include('library.urls')),
        url(r'^$', views.splash, name='splash'),  
        url(r'^library/', include('library.urls')),
        url(r'^about/', views.about, name='about'),
        url(r'^admin/', admin.site.urls),
]
