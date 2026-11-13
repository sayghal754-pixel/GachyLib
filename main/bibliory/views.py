from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET

from .models import Book


def home(request):
    books = Book.objects.all()
    query = request.GET.get('q', '').strip()
    if query:
        books = books.filter(title__icontains=query)
    paginator = Paginator(books, 12)
    page = paginator.get_page(request.GET.get('page'))
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        response = render(request, 'bibliory/_book_list.html', {'page': page})
        response['X-Has-Next'] = str(page.has_next()).lower()
        return response
    return render(request, 'bibliory/home.html', {'page': page, 'query': query})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'bibliory/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm(request)
    return render(request, 'bibliory/login.html', {'form': form})


@require_GET
def read_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if not book.file:
        raise Http404('Для этой книги файл не загружен.')
    extension = book.file.name.rsplit('.', 1)[-1].lower() if '.' in book.file.name else ''
    context = {'book': book, 'reader_type': extension}
    if extension == 'txt':
        try:
            with book.file.open('rb') as source:
                context['text'] = source.read().decode('utf-8-sig')
        except UnicodeDecodeError:
            with book.file.open('rb') as source:
                context['text'] = source.read().decode('cp1251', errors='replace')
    return render(request, 'bibliory/reader.html', context)
