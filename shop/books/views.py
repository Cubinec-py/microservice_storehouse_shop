from django.views import generic

from django.db.models import Max, Min

from books.models import Book
from books.filter import BookFilter


class AllBooksListView(generic.ListView):
    model = Book
    template_name = 'shop/store.html'
    ordering = ['-created']
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = BookFilter(self.request.GET, queryset=self.get_queryset())

        context['min_price'] = Book.objects.aggregate(Min('price'))
        context['max_price'] = Book.objects.aggregate(Max('price'))

        return context


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book/book_detail.html'
