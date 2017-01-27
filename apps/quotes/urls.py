from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^registration$', views.registration),
    url(r'^success$', views.success),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^delete_all_objects$', views.delete),
    url(r'^add_quote$', views.add_quote),
    url(r'^show/user/(?P<user_id>\d+)$', views.view_user, name= 'view_user'),
    url(r'^addfav/(?P<quote_id>\d+)$', views.add_fav, name= 'add_fav'),
    url(r'^removefav/(?P<quote_id>\d+)$', views.rem_fav, name= 'rem_fav'),

]
