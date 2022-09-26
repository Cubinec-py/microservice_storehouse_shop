from django.db import models

from books.models import Book, BookItem

ORDER_STATUS = (
    ('Processing', 'Processing'),
    ('Packing', 'Packing'),
    ('Delivering', 'Delivering'),
    ('Canceled', 'Canceled'),
    ('Completed', 'Completed'),
)


class Order(models.Model):
    customer_email = models.EmailField(max_length=50, help_text='Email to contact with customer')
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=ORDER_STATUS,
        max_length=100,
        help_text='Status of order from storehouse',
        null=True)
    transaction_id = models.CharField(max_length=100, null=True, unique=True)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, to_field='transaction_id', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)


class OrderItemBookItem(models.Model):
    book_item = models.ForeignKey(BookItem, on_delete=models.SET_NULL, null=True, help_text='Taking book from store')
    order_item = models.ForeignKey(OrderItem, on_delete=models.SET_NULL, null=True)


class ShippingAddress(models.Model):
    order = models.ForeignKey(Order, to_field='transaction_id', on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.address
