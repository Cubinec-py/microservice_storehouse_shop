from rest_framework import serializers

from books.models import Book, BookItem, Author, Genre


class BookItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookItem
        fields = ['count']


class BookSerializer(serializers.HyperlinkedModelSerializer):
    count_value = serializers.SerializerMethodField()
    genre = serializers.StringRelatedField(many=True)
    author_first_name = serializers.ReadOnlyField(source="author.first_name")
    author_last_name = serializers.ReadOnlyField(source="author.last_name")

    def get_count_value(self, instance):
        data_models = BookItem.objects.filter(book=instance)
        serializer = BookItemSerializer(instance=data_models, many=True, read_only=True)

        return serializer.data

    class Meta:
        model = Book
        fields = [
            'url', 'custom_id', 'title', 'author_first_name', 'author_last_name', 'description',
            'genre', 'price', 'pages', 'count_value']


class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Author
        fields = ['url', 'first_name', 'last_name']


class GenreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Genre
        fields = ['url', 'name']
