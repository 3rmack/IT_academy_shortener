from django.conf.urls import url
from . import views


urlpatterns = [
    # url(r'^\?s=', views.go, name='go'),
    url(r'^$', views.index, name='index'),
]
