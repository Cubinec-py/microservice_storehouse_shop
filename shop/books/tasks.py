import requests

from celery import shared_task

from books.models import Book, Genre, Author


@shared_task
def check_for_books():
    print('Starting for updating books')
    url = 'http://127.0.0.1:8001/api/book/'
    page = ''

    while True:
        try:
            base = requests.get(url + page)
        except requests.exceptions.ConnectionError:
            return 'No internet connection!'
        soup = base.json()

        for elements in soup['results']:
            if Book.objects.filter(storehouse_book_id=elements['id']) is not None:

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

        try:
            page = soup['next'].split('/')[-1]
        except AttributeError:
            print('All new books added')
            break


@shared_task
def update_count_books():
    print('Updating for count of books')
    url = 'http://127.0.0.1:8001/api/book/'
    page = ''

    while True:
        try:
            base = requests.get(url + page)
        except requests.exceptions.ConnectionError:
            return 'No internet connection!'
        soup = base.json()

        for elements in soup['results']:
            if not Book.objects.filter(storehouse_book_id=elements['id'], count=elements['count_value']):
                Book.objects.filter(storehouse_book_id=elements['id']).update(count=elements['count_value'])

        try:
            page = soup['next'].split('/')[-1]
        except AttributeError:
            print('All books updated')
            break
