from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^show/(?P<user_id>\d+)', views.show_user, name='show_user'),
    url(r'^new', views.new_user_admin, name='new_user_admin'),
    url(r'^edit/(?P<user_id>\d+)', views.edit_user_admin, name='edit_user_admin'),
    url(r'^edit', views.edit_user, name='edit_user'),
    url(r'^destroy/(?P<user_id>\d+)', views.destroy_user_admin, name='destroy_user_admin'),
    url(r'^create', views.create_user_admin, name='create_user_admin'),
    url(r'^update/(?P<user_id>\d+)', views.update_user, name='update_user'),
    url(r'^', views.index, name='index'),
]
