import requests

from django.core.mail import send_mail

from celery import shared_task

from order.models import Order, OrderItem, ShippingAddress

from secret_token import token_value


@shared_task
def order_to_storehouse(customer_email, transaction_id):
    print(f'Sending order with transaction_id:{transaction_id} to storehouse')
    order = Order.objects.filter(transaction_id=transaction_id)
    order_items = OrderItem.objects.filter(order__in=order)
    address = ShippingAddress.objects.filter(order__in=order)

    data_order_item = []

    for item in order_items:
        data_order_item.append({
            "book": item.book.storehouse_book_id,
            "quantity": item.quantity,
            "order": transaction_id,
        })

    data_order = {
        "customer_email": customer_email,
        "transaction_id": transaction_id,
    }

    try:
        requests.post(
            'http://storehouse:8000/api/order/',
            headers={'Authorization': f'Token {token_value}'},
            json=data_order
        )
    except requests.exceptions.ConnectionError:
        return 'No internet connection to order!'

    try:
        requests.post(
            'http://storehouse:8000/api/order_item/',
            headers={'Authorization': f'Token {token_value}'},
            json=data_order_item
        )
    except requests.exceptions.ConnectionError:
        return 'No internet connection to order_item!'

    for item in address:
        data_order_address = {
            "order": transaction_id,
            "address": item.address,
            "city": item.city,
            "state": item.state,
            "zipcode": item.zipcode
        }

        try:
            requests.post(
                'http://storehouse:8000/api/shipping_address/',
                headers={'Authorization': f'Token {token_value}'},
                json=data_order_address
            )
        except requests.exceptions.ConnectionError:
            return 'No internet connection to shipping_address!'


@shared_task
def check_order_status(order_id):
    print(f'Updating status of order_id: {order_id}.')
    url = 'http://storehouse:8000/api/order/'
    page = ''
    while True:
        try:
            base = requests.get(url + page, headers={'Authorization': f'Token {token_value}'})
        except requests.exceptions.ConnectionError:
            print('No internet connection!')
            break
        soup = base.json()

        for elements in soup['results']:
            order = Order.objects.filter(id=order_id)
            for item in order:
                if elements['transaction_id'] == item.transaction_id:
                    try:
                        Order.objects.filter(id=item.id).update(status=elements['status'])
                    except TypeError:
                        print('Type Error')
                        break
        try:
            page = soup['next'].split('/')[-1]
        except AttributeError:
            return print('Order status updated.')


def confirm_order_email(customer_email, transaction_id, customer_name):
    email = customer_email
    subject = f'Yor order was successfully created!'
    message = f'Hi {customer_name}!\n' \
              f'Your order number is {transaction_id}. \n' \
              f'You can copy this number, go to "My orders", past it in the search field and see your order details.'
    from_email = 'admin@admin.admin'
    send_mail(subject, message, from_email, [email], fail_silently=False)
