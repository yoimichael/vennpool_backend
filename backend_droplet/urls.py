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
from gepu.views import remove_auth_token, get_auth_token, create_user, users_detail, post_list, post_detail, event_list,get_hash, get_event

# default index page
from django.http import HttpResponse
def index(request):
    return HttpResponse("Hello, Vennpool.")

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index,name='index'),
    url(r'^api/login/$', get_auth_token),
    url(r'^api/logout/$', remove_auth_token),
    url(r'^api/user/$', create_user),
    url(r'^api/user/(?P<id>[0-9]+)$', users_detail),
    url(r'^api/post/$', post_list),
    url(r'^api/post/(?P<id>[0-9]+)$', post_detail),
    url(r'^api/event/$', event_list),
    url(r'^api/hash/code/(?P<hash_code>[.]{4})$', get_event),
    url(r'^api/hash/event/(?P<event_id>[0-9,]+)$', get_hash),
]
