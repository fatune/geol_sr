from django.conf.urls import url
from sr import views

urlpatterns = [
    url(r'^(?P<subject_id>\d+)/$', views.study, name='study'),
    url(r'^$', views.study_list, name='study list'),
]


