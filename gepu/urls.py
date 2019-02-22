from django.conf.urls import url

# -------front-back test/
# import gepu's views
from .views import users_list, users_detail, index_prompt


# url('', views.index, name = 'index'),
urlpatterns = [
    url('', index_prompt,name='index'),
    url(r'^api/gepu/$', users_list),
    url(r'^api/gepu/(?P<pk>[0-9]+)$', users_detail),
]
