from django.utils import translation
from django.db import models
from django.db.models import Q
from polyglot import defaults
from polyglot import helpers
import operator

class LanguageFieldManager(models.Manager):
    """Returns elements of the current language. Use this manager when
    your model has a MANAGER_LANG_FIELD.

    """

    def lall(self):
        """Similar to cls.all() but with a lang filter"""
        lang = translation.get_language()[:2]
        filterby = {str(defaults.MANAGER_LANG_FIELD): lang}
        return self.get_query_set().filter(**filterby)


class LanguageManager(models.Manager):
    """Returns elements of the current language. Use this manager when
    you have different fields for different languages

    """

    def __init__(self, *fields):
        super(LanguageManager, self).__init__()
        self.fields = fields

    def lall(self, *fields):
        """Similar to cls.all() but with a lang filter"""
        if not fields:
            fields = self.fields
        qlist = []
        for field in fields:
            field_name = helpers.format_field_name(field)
            qlist.append(Q(**{field_name: ''}))
        if qlist:
            return self.get_query_set().exclude(reduce(operator.or_, qlist))
        else:
            return self.get_query_set()
