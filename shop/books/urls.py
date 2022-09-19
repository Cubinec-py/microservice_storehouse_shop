from django.urls import path

from books.views import AllBooksListView, BookDetailView

urlpatterns = [
    path('', AllBooksListView.as_view(), name="store"),
    path('detail/<pk>', BookDetailView.as_view(), name="book_detail"),
]
