from django.conf import settings

# name of the field that holds the object's language
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
