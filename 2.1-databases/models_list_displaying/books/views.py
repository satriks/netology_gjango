from django.shortcuts import render, redirect

from books.models import Book


def index(request):
    return redirect('books')

def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all
    context = {'books': books}
    return render(request, template, context)

def book_date(request, pub_date):
    template = 'books/books_list.html'
    books = Book.objects.filter(pub_date=pub_date).all()
    prev_page = Book.objects.order_by('-pub_date').filter(pub_date__lt=pub_date).first()
    next_page = Book.objects.order_by('pub_date').filter(pub_date__gt=pub_date).first()
    context = {'books': books, 'prev_page': prev_page, 'next_page' : next_page}
    return render(request, template, context)
