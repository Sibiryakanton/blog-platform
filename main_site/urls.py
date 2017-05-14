from django.conf.urls import url
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^blogs/(?P<username>[-\w]+)/$', views.blog_page, name='blog_page'),
	url(r'^add_post/$', views.add_post, name='add_post'),
	url(r'^note/(?P<post_id>\d+)/$', views.note, name='note'),
	url(r'^subscribe/(?P<username>[-\w]+)/$', views.subscribe, name='subscribe'),
	url(r'^unsubscribe/(?P<username>[-\w]+)/$', views.unsubscribe, name='unsubscribe'),
	url(r'^logout/$', views.exit, name='logout'),
	url(r'^login/$', views.enter, name='login'),
]
