# ~*~ coding: utf-8 ~*~
from faq.models import FaqCategories, FaqAnswers
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.http import Http404
from decorators import render_to

@render_to('faq/index.html')
def index(request):
    cats = FaqCategories.objects.all().order_by('id')
    for cat in cats:
        cat.answers = FaqAnswers.objects.filter(category=cat.id).order_by('-id')
    return {'cats': cats}


@render_to('faq/category.html')
def category(request, id):
    try:
        category = FaqCategories.objects.get(pk=id)
    except FaqCategories.DoesNotExist:
        raise Http404
    try:
        answers = FaqAnswers.objects.filter(category=id).order_by('id')
    except FaqAnswers.DoesNotExist:
        raise Http404
    return {'category': category,
            'answers': answers}


@render_to('faq/answer.html')
def answer(request, category, id):
    category = FaqCategories.objects.get(pk=category)
    try:
        answer = FaqAnswers.objects.get(pk=id)
    except FaqAnswers.DoesNotExist:
        raise Http404
    return {'category': category,
            'answer': answer}


class rss(Feed):
    title = "Последние статьи easy-dns.ru"
    link = "http://easy-dns.ru/faq/"
    description = "Статьи и обзоры сервиса регистрации доменных имен easy-dns.ru"
    author_link = "http://easy-dns.ru"

    def items(self):
        return FaqAnswers.objects.all().order_by('-id')

    def item_title(self, item):
        return item.question

    def item_description(self, item):
        return item.answer

    def item_link(self, item):
        return 'http://easy-dns.ru' + reverse('faq.views.answer', args=[item.category_id, item.id])