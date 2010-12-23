"this is the locale selecting middleware that will look at accept headers"

from django.conf import settings
from django.utils.cache import patch_vary_headers
from django.utils import translation
from polyglot.defaults import FORCE_LANG_PARAM


class LocaleMiddleware(object):
    """This is a very simple middleware that parses a request and
    decides what translation object to install in the current thread
    context. This allows pages to be dynamically translated to the
    language the user desires (if the language is available, of
    course).

    """

    def process_request(self, request):
        languages = [l[0] for l in settings.LANGUAGES]
        force_lang = request.GET.get(FORCE_LANG_PARAM, False)
        language = None

        if force_lang in languages: language = force_lang

        if not language:
            language = translation.get_language_from_request(request)

        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        patch_vary_headers(response, ('Accept-Language',))
        if 'Content-Language' not in response:
            response['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response
