from django.views import generic

from books.models import Book


class AllBooksListView(generic.ListView):
    model = Book
    template_name = 'book/store.html'
    ordering = ['-created']
    paginate_by = 9


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book/book_detail.html'
