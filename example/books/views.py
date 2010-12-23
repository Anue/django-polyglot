from books.models import Book
from django.shortcuts import render_to_response
from django.utils.translation import to_locale, get_language


def books(request, lang='en'):
    locale = to_locale(get_language()).lower()[:2]
    return render_to_response('books/books.html', {'books': Book.objects.all()})
