import requests

from celery import shared_task

from order.models import Order, OrderItem, ShippingAddress


@shared_task
def order_to_storehouse(customer, transaction_id):
    order = Order.objects.filter(transaction_id=transaction_id)
    order_items = OrderItem.objects.filter(order__in=order)
    address = ShippingAddress.objects.filter(order=order)

    data_order_item = []

    data_order = {
        "customer_email": customer.email,
        "transaction_id": transaction_id,
    }

    for item in order_items:
        data_order_item.append({
            "book": item.book.storehouse_book_id,
            "quantity": item.quantity,
            "order": transaction_id,
        })

    requests.post(
        'http://127.0.0.1:8000/api/order/',
        headers={'Authorization': 'Token bccffe02287b3ba51e5e8d4a31b7a5c755176ab6'},
        json=data_order
    )

    requests.post(
        'http://127.0.0.1:8000/api/order_item/',
        headers={'Authorization': 'Token bccffe02287b3ba51e5e8d4a31b7a5c755176ab6'},
        json=data_order_item
    )

    for item in address:
        data_order_address = {
            "order": transaction_id,
            "address": item.address,
            "city": item.city,
            "state": item.state,
            "zipcode": item.zipcode
        }

        requests.post(
            'http://127.0.0.1:8000/api/shipping_address/',
            headers={'Authorization': 'Token bccffe02287b3ba51e5e8d4a31b7a5c755176ab6'},
            json=data_order_address
        )
