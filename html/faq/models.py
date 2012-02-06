# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

class FaqCategories(models.Model):
    name =  models.CharField(max_length=255)
    def __unicode__( self ):
        return self.name
    
class FaqAnswers(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    answer_short = models.TextField(default='')
    post_date = models.DateTimeField(auto_now_add=True, db_index=True)
    category = models.ForeignKey(FaqCategories, null=True)
    def __unicode__( self ):
        return self.question
