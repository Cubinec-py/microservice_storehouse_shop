import requests

from celery import shared_task

from books.models import Book, Genre, Author

from secret_token import token_value


@shared_task
def check_for_books():
    print('Starting for updating books')
    url = 'http://storehouse:8000/api/book/'
    page = ''

    while True:
        try:
            base = requests.get(url + page, headers={'Authorization': f'Token {token_value}'})
        except requests.exceptions.ConnectionError:
            return 'No internet connection!'
        soup = base.json()

        try:
            for elements in soup['results']:
                if not Book.objects.filter(storehouse_book_id=elements['id']).exists():

                    auth_obj, created = Author.objects.get_or_create(
                        first_name=elements['author_first_name'],
                        last_name=elements['author_last_name'],
                    )

                    book_obj, created = Book.objects.get_or_create(
                        title=elements['title'],
                        description=elements['description'],
                        price=elements['price'],
                        pages=elements['pages'],
                        count=elements['count_value'],
                        created=elements['created'],
                        author=auth_obj,
                        storehouse_book_id=elements['id'],
                    )

                    for item in elements['genre_list']:
                        genre_obj, created = Genre.objects.get_or_create(
                            name=item['name']
                        )
                        book_obj.genre.add(genre_obj)

        except TypeError:
            return print('TypeError')

        try:
            page = soup['next'].split('/')[-1]
        except AttributeError:
            return print('All new books added')


@shared_task
def update_count_books():
    print('Updating for count of books')
    url = 'http://storehouse:8000/api/book/'
    page = ''

    while True:
        try:
            base = requests.get(url + page, headers={'Authorization': f'Token {token_value}'})
        except requests.exceptions.ConnectionError:
            return 'No internet connection!'
        soup = base.json()

        try:
            for elements in soup['results']:
                if not Book.objects.filter(storehouse_book_id=elements['id'], count=elements['count_value']):
                    Book.objects.filter(storehouse_book_id=elements['id']).update(count=elements['count_value'])
        except TypeError:
            return print('TypeError')
        try:
            page = soup['next'].split('/')[-1]
        except AttributeError:
            return print('All books updated')
