"""bierklub URL Configuration

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
"""
from django.conf.urls import include, url
from django.contrib import admin

import klubevents.views

urlpatterns = [
    url(r'^$', klubevents.views.IndexView.as_view()),
    url(r'^events/', include('klubevents.urls')),
    url(r'^admin/', admin.site.urls),
]

handler404 = 'error_handlers.views.standard_404'
handler500 = 'error_handlers.views.standard_500'

# if you want Django to serve static files for you through nginx, you can use
# this
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# urlpatterns += staticfiles_urlpatterns()
