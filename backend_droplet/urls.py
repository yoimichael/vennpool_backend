"""backend_droplet URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin

# API call imports
from gepu.user_views import users_list, users_detail

# default index page
from django.http import HttpResponse
def index(request):
    return HttpResponse("Hello, Vennpool.")


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index,name='index'),
    url(r'^api/user/$', users_list),
    url(r'^api/user/(?P<id>[0-9]+)$', users_detail),
]
