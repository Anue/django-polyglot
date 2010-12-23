Django Polyglot
===============

About
-----

Django Polyglot is a small app with a bunch of utilities that make
database based translation and working with languages in general
easier within the Django Web framework.

Installation
------------

The recommended way to install django-polyglot is using pip.

You can do this by adding a line like this in your requirements.txt::

    -e git://github.com/Anue/django-polyglot.git#egg=polyglot

The other way to install it is adding the 'polyglot' folder in your
django app's folder of your django project.

After that just include 'polyglot' in your INSTALLED_APPS settings.

Settings
========

POLYGLOT_MANAGER_LANG_FIELD (default: "language")::
    name of the field that holds the object's language
    this is only useful when translations are stored in different
    instances and each instance contain a field which stores the
    language code for it

POLYGLOT_FIELD_FORMAT (default: "suffix")::
    default behavior when normalizing a field name
    'prefix' should be used when fields are named as <lang>_<field_name>
    'suffix' should be used when fields are named as <field_name>_<lang>

POLYGLOT_GETTER_PREFIX (default: "get")::
    default prefix for methods created by the decorators
    methods will be named GETTER_PREFIX + _ + <field_name>

POLYGLOT_SETTER_PREFIX (default: "set"):
    default prefix for methods created by the decorators
    methods will be named SETTER_PREFIX + _ + <field_name>
    name of the GET param that will force current language

POLYGLOT_FORCE_LANG_PARAM (default: "lang")::
    name of the GET param that will force current language

Optional extra setup
====================

middleware
~~~~~~~~~~

You can add polyglot.middleware.LocaleMiddleware to MIDDLEWARE_CLASSES
setting to activate polyglot's force language middleware which allows
to override the current active language via url using the value of
POLYGLOT_FORCE_LANG_PARAM

for instance:

<site.domain>/books/?lang=es

Will force the language to use spanish (es) if available in the
LANGUAGES setting. If not will use the default Django machinery to get
the language from the request.


Polyglot's normalize* decorators:
---------------------------------

Polyglot offer 4 decorators that simplify handling database field
based translations.

We say the POLYGLOT_FORMAT_FIELD should be 'prefix' when language
codes are before the real field name (example: en_name) and should be
'suffix' when codes are after the real field name (example: name_en)

For examples we'll use the following models::

    class SuffixExample(models.Model):
        name_en = models.CharField(max_length=32)
        name_es = models.CharField(max_length=32)

    class PrefixExample(models.Model):
        en_name = models.CharField(max_length=32)
        es_name = models.CharField(max_length=32)

After appliying polyglot's decorators correctly any instances of these
models will have a 'name' property which will access 'en' or 'es'
based on the active language like this::

    >>> from django.utils import translation
    >>> s = SuffixExample(name_en='test', name_es='prueba')
    >>> s.save()
    >>> translation.get_language()
    'en'
    >>> s.name
    'test'
    >>> translation.activate('es')
    >>> translation.get_language()
    'es'
    >>> s.name
    'prueba'
    >>> s.name = 'pruebacambiada'
    >>> s.save()
    >>> s.name
    'pruebacambiada'
    >>> s.name_en
    'test'
    >>> s.name_es
    'pruebacambiada'

The auto_normalize decorator
============================

The auto_normalize decorator can be applied on any model class that
respects the POLYGLOT_FIELD_FORMAT setting specified. It will scan for
all translatable fields and will setup descriptors automatically.

For instance, given that POLYGLOT_FIELD_FORMAT equals to 'suffix' this
will work::

    @auto_normalize
    class SuffixExample(models.Model):

However this will not, since POLYGLOT_FIELD_FORMAT is not 'prefix'::

    @auto_normalize
    class PrefixExample(models.Model):

The auto_normalize decorator_prefix
===================================

The auto_normalize_prefix decorator can be applied on any model class
uses a prefixed field format not taking in account the value of
POLYGLOT_FIELD_FORMAT.

For instance, this wouldn't work since the field format for
SuffixExample is 'suffix'::

    @auto_normalize_prefix
    class SuffixExample(models.Model):

While this will work cool::

    @auto_normalize_prefix
    class PrefixExample(models.Model):

The auto_normalize decorator_suffix
===================================

The auto_normalize_suffix decorator can be applied on any model class
uses a suffixed field format not taking in account the value of
POLYGLOT_FIELD_FORMAT.

For instance, this wouldn't work since the field format for
PrefixExample is 'prefix'::

    @auto_normalize_suffix
    class PrefixExample(models.Model):

While this will work cool::

    @auto_normalize_suffix
    class SuffixExample(models.Model):

The normalize decorator
=======================

The normalize decorator allows to explicitly passing the fields that
should be normalized so no calculation takes place, this way
performance is enhanced for large models.

By default it takes the field format from POLYGLOT_FIELD_FORMAT
setting but it can be overriden via the field_format keyword
argument::

    @normalize('name', format_field='suffix')
    class SuffixExample(models.Model):

    ...

    @normalize('name', format_field='prefix')
    class PrefixExample(models.Model):


Polyglot's Managers
-------------------

Polyglot's provides two managers intended to ease the retrieval of all
objects for the current activated language via Model.objects.lall()
method.


LanguageFieldManager
====================

Useful for when all translations are saved on separated instances and
the language for each instance is saved in the field specified in the
POLYGLOT_MANAGER_LANG_FIELD.


LanguageManager
===============

Useful for when all translations are saved on a suffix/prefix based
approach on same instances. It will return objects for the current
language when specified translatable fields are not empty.


TBD: explain urls, templatetags and management commands
