from django.shortcuts import render_to_response
from books.models import Book

def books(request):
    return render_to_response('books/books.html', {'books': Book.objects.all()})
