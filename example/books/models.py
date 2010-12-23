from django.db import models
from polyglot.decorators import *


@auto_normalize_prefix
class Book(models.Model):

    en_name = models.CharField(max_length=128)
    es_name = models.CharField(max_length=128)
    en_description = models.CharField(max_length=128)
    es_description = models.CharField(max_length=128)
    isbn = models.CharField(max_length=16)

    def __unicode__(self):
        return self.es_name
