from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^list', views.activity_list, name='activity list'),
    url(r'^(?P<activity_id>\d+)/$', views.activity_item, name="activity item"),
    url(r'^new', views.create_activity, name="create activity"),
    url(r'^(?P<activity_id>\d+)/update', views.update_activity, name="update activity"),
    url(r'^(?P<activity_id>\d+)/delete', views.del_activity, name="delete activity"),
    url(r'^(?P<activity_id>\d+)/join', views.join_activity, name="join activity"),
    url(r'^(?P<activity_id>\d+)/quit', views.quit_activity, name="quit activity"),
]