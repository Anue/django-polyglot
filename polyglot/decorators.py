import functools

from django.utils import translation
from polyglot import defaults, helpers


__all__ = ['auto_normalize', 'auto_normalize_prefix', 'auto_normalize_suffix', 'normalize']

def __get_field_name(self, normalized_field_name, field_format=defaults.FIELD_FORMAT):
    """get the actual field name from the normalized field name and
    the language.

    """
    current_language = translation.get_language()[:2]
    if field_format == 'prefix':
        field_name = "%s_%s" % (current_language, normalized_field_name)
    elif field_format == 'suffix':
        field_name = "%s_%s" % (normalized_field_name, current_language)
    return field_name

def __set_descriptor(cls, normalized_field_name, field_format=defaults.FIELD_FORMAT):
    """Set descriptor for field names with translation fields"""
    getter_name = "%s_%s" % (defaults.GETTER_PREFIX, normalized_field_name)
    setter_name = "%s_%s" % (defaults.SETTER_PREFIX, normalized_field_name)
    setattr(cls, '__get_field_name', __get_field_name)
    setattr(cls, getter_name,
            lambda cls, field_name=normalized_field_name, field_format=field_format: \
            getattr(cls, getattr(cls, '__get_field_name')(field_name, field_format))
    )
    setattr(cls, setter_name,
            lambda cls, value, field_name=normalized_field_name, field_format=field_format: \
            setattr(cls, getattr(cls, '__get_field_name')(field_name, field_format), value)
    )
    setattr(cls, normalized_field_name, property(getattr(cls, getter_name),getattr(cls, setter_name)))

def __auto_normalize(field_format=defaults.FIELD_FORMAT, *args, **kwargs):
    """Automatically Creates properties for the fields on the
    decorated class which allow accessing to the correct i18nized
    field according the selected language.

    For instance if the language is 'en' and you have en_mytable, you
    could access that specific field through the mytable property.

    """
    def wrap(cls):
        current_language = translation.get_language()[:2]
        fields = [f.name for f in cls._meta.local_fields]
        possible_prefix = "%s_" % current_language
        possible_suffix = "_%s" % current_language
        for field_name in fields:
            if field_name.startswith(possible_prefix) or field_name.endswith(possible_suffix):
                normalized_field_name = helpers.normalize_field_name(field_name, field_format)
                __set_descriptor(cls, normalized_field_name, field_format)
        return cls
    return wrap

auto_normalize = functools.partial(__auto_normalize)()
auto_normalize_prefix = functools.partial(__auto_normalize, field_format='prefix')()
auto_normalize_suffix = functools.partial(__auto_normalize, field_format='suffix')()

def normalize(*fields, **kwargs):
    """Creates properties for the fields passed as parameters on the
    decorated class which allow accessing to the correct i18nized
    field according the selected language.

    For instance if the language is 'en' and you have en_mytable, you
    could access that specific field through the mytable property.

    """
    field_format = kwargs.get('field_format', defaults.FIELD_FORMAT)
    def wrap(cls):
        for normalized_field_name in fields:
            field_name = helpers.format_field_name(normalized_field_name, field_format)
            __set_descriptor(cls, normalized_field_name, field_format)
        return cls
    return wrap
