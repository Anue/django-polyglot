from django.conf.urls.defaults import *


urlpatterns = patterns(
    'books.views',
    url(r'^$', 'books', name='books_home'),
)
