from django.contrib import admin
from django.contrib.admin import TabularInline, StackedInline

from books.models import Genre, Book, BookItem, Author


class BookItemInline(StackedInline):
    model = BookItem
    fields = ('book', 'imprint')
    extra = 1


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price')
    list_filter = ['title', 'author', 'price', 'genre']
    inlines = [BookItemInline]
    filter_horizontal = ('genre',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']
    list_filter = ['last_name']
    search_fields = ['first_name', 'last_name']


@admin.register(BookItem)
class BookItemAdmin(admin.ModelAdmin):
    list_display = ['book', 'imprint', 'status']
    list_filter = ['status', 'book']
    search_fields = ['imprint', 'book']
