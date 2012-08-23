# -*- coding: utf-8 -*-
from decorators import render_to
from news.models import News
from faq.models import FaqCategories, FaqAnswers

@render_to('index.html')
def index(request):
    return {}


@render_to('about.html')
def about(request):
    return {}