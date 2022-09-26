from rest_framework import serializers

from books.models import Book, BookItem, Author, Genre


class BookItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookItem
        fields = ['book', 'imprint']


class BookSerializer(serializers.ModelSerializer):
    count_value = serializers.SerializerMethodField()
    genre_list = serializers.SerializerMethodField()
    author_first_name = serializers.ReadOnlyField(source="author.first_name")
    author_last_name = serializers.ReadOnlyField(source="author.last_name")

    def get_count_value(self, instance):
        get_book = Book.objects.get(title=instance)
        data_models = get_book.bookitem_set.count()

        return data_models

    def get_genre_list(self, instance):
        data_models = Genre.objects.filter(book=instance)
        serializer = GenreSerializer(instance=data_models, many=True, read_only=True)

        return serializer.data

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'author_first_name', 'author_last_name', 'description',
            'genre_list', 'price', 'pages', 'count_value', 'created']


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['first_name', 'last_name']


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ['id', 'name']
