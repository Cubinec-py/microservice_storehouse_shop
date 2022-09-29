from django.contrib import admin
from django.contrib.admin import TabularInline, StackedInline

from order.models import Order, OrderItem, ShippingAddress
from books.models import BookItem

from order.tasks import order_status_email


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    filter_horizontal = ('book_item',)


class ShippingAddressInline(StackedInline):
    model = ShippingAddress
    readonly_fields = ['address', 'city', 'state', 'zipcode']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_email', 'status', 'transaction_id']
    list_filter = ['id']
    inlines = [ShippingAddressInline, OrderItemInline]
    search_fields = ['transaction_id']

    def save_model(self, request, obj, form, change):
        status_obj = Order.objects.filter(id=obj.id)
        value = ''
        for i in status_obj:
            value = i.status
        super().save_model(request, obj, form, change)
        status = obj.status
        transaction_id = obj.transaction_id
        email = obj.customer_email
        if value != obj.status:
            order_status_email(transaction_id, status, email, value)
        if obj.status:
            for element in obj.orderitem_set.all():
                for item in element.book_item.all():
                    BookItem.objects.filter(id=item.id).update(status='Unavailable')
