from django.conf.urls.defaults import *
from news.views import rss

urlpatterns = patterns('news.views',
    (r'^$', 'index'),
    (r'^(?P<new_id>\d+)/$', 'details'),
    (r'^rss/$', rss()),
)

