# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('my.views',
    (r'^$', 'index'),
    (r'^new/$', 'new'),
    (r'^feedtest/$', 'feedtest'),
    (r'^sync/(?P<syncid>\d+)/$', 'sync'),
    (r'^sync/(?P<syncid>\d+)/remove$', 'delsync'),
    (r'^sync/(?P<syncid>\d+)/vk/$', 'syncvk'),
    (r'^sync/(?P<syncid>\d+)/twitter/$', 'synctwitter'),
    (r'^sync/(?P<syncid>\d+)/fb/$', 'syncfacebook'),
    (r'^sync/(?P<syncid>\d+)/fs/$', 'syncfoursqare'),
    (r'^sync/(?P<syncid>\d+)/delete/(?P<ppid>\d+)/$', 'deldest'),
    (r'^profile/$', 'profile'),
                       )
