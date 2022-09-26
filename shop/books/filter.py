import django_filters
from django_filters import RangeFilter

from books.models import Book


class BookFilter(django_filters.FilterSet):
    price = RangeFilter()

    class Meta:
        model = Book
        exclude = ['image']
        fields = {
            'price': [],
            'title': ['icontains'],
            'genre': ['exact'],
            'author': ['exact']
        }
