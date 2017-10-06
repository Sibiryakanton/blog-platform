from django.conf.urls import url
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^$', views.index.as_view(), name='index'),
    url(r'^(?P<ordering>[-\w]+)/$', views.index.as_view(), name='index2'),
    url(r'^blogs/(?P<username>[-\w]+)/$', views.blog_page.as_view(), name='blog_page'),
    url(r'^blogs/(?P<username>[-\w]+)/(?P<post_pk>[0-9]+)/$', views.post_page.as_view(), name='post_page'),
    url(r'^add_post/$', views.add_post.as_view(), name='add_post'),
    url(r'^edit_post/(?P<username>[-\w]+)/(?P<post_pk>[0-9]+)/$', views.edit_post.as_view(), name='edit_post'),
    url(r'^note/(?P<post_id>\d+)/$', views.note.as_view(), name='note'),
    url(r'^subscribe/(?P<user_name>[-\w]+)/$', views.subscribe.as_view(), name='subscribe'),
    url(r'^unsubscribe/(?P<user_name>[-\w]+)/$', views.unsubscribe.as_view(), name='unsubscribe'),
    url(r'^logout/$', views.exit.as_view(), name='logout'),
    url(r'^login/$', views.enter.as_view(), name='login'),
]
