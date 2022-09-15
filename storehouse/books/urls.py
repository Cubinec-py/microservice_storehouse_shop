from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books import views

router = DefaultRouter()
router.register(r'book', views.BookViewSet, basename="book")
router.register(r'book_item', views.BookItemViewSet, basename="bookitem")
router.register(r'author', views.AuthorViewSet, basename="author")
router.register(r'genre', views.GenreViewSet, basename="genre")


urlpatterns = [
    path('', include(router.urls)),
]
