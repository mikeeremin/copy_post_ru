from django.db import models

class News(models.Model):
    pdate = models.DateTimeField()
    title = models.CharField(max_length=200)
    announce = models.CharField(max_length=1000)
    text = models.TextField()

    def __unicode__( self ):
        return self.title