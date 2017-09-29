from django.conf.urls import url
from sr import views

urlpatterns = [
    url(r'^(?P<value>\d+)/$', views.study, name='study'),
]


