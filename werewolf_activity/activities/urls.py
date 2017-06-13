from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^list', views.activity_list, name='activity list'),
]