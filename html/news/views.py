# ~*~ coding: utf-8 ~*~
from django.shortcuts import render_to_response
from news.models import News
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.http import Http404
from decorators import render_to

@render_to('news/index.html')
def index(request):
    news = News.objects.all().order_by('-pdate')
    return {'news': news}

@render_to('news/details.html')
def details(request, new_id):
    try:
        new = News.objects.get(pk = new_id)
        return {'new': new}
    except News.DoesNotExist:
        raise Http404


class rss(Feed):
    title = "Copy-post. Синхронизируем все!"
    link = "http://copy-post.ru/news/"
    description = "Новости сервиса copy-post.ru"
    author_link = "http://copy-post.ru"
    def items(self):
        return News.objects.all().order_by('-pdate')
    
    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.announce 

    def item_link(self, item):
        return 'http://copy-post.ru' + reverse('news.views.details', args=[item.id])