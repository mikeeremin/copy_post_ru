# -*- coding: utf-8 -*-

from faq.models import FaqCategories, FaqAnswers
from django.contrib import admin

admin.site.register(FaqCategories)
admin.site.register(FaqAnswers)