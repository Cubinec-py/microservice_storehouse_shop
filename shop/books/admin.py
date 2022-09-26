from django.contrib import admin

from books.models import Genre, Book, Author


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price')
    list_filter = ['title', 'author', 'price', 'genre']
    search_fields = ['title']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']
    list_filter = ['last_name']
    search_fields = ['first_name', 'last_name']
