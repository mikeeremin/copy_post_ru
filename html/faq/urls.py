from django.conf.urls.defaults import *
from faq.views import rss

urlpatterns = patterns('faq.views',
    (r'^$', 'index'),
    (r'^(?P<id>\d+)/$', 'category'),
    (r'^(?P<category>\d+)/(?P<id>\d+)/$', 'answer'),
    (r'^rss/$', rss()),
)
