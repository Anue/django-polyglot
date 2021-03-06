from django.conf import settings

# name of the field that holds the object's language
# this is only useful when translations are stored in different
# instances and each instance contain a field which stores the
# language code for it
MANAGER_LANG_FIELD = getattr(settings, "POLYGLOT_MANAGER_LANG_FIELD", 'language')

# default behavior when normalizing a field name
# 'prefix' should be used when fields are named as <lang>_<field_name>
# 'suffix' should be used when fields are named as <field_name>_<lang>
FIELD_FORMAT = getattr(settings, "POLYGLOT_FIELD_FORMAT", 'suffix')

# default prefix for methods created by the decorators
# methods will be named GETTER_PREFIX + _ + <field_name>
GETTER_PREFIX  = getattr(settings, "POLYGLOT_GETTER_PREFIX", 'get')

# default prefix for methods created by the decorators
# methods will be named SETTER_PREFIX + _ + <field_name>
SETTER_PREFIX  = getattr(settings, "POLYGLOT_SETTER_PREFIX", 'set')

# name of the GET param that will force current language
FORCE_LANG_PARAM  = getattr(settings, "POLYGLOT_FORCE_LANG_PARAM", 'lang')
