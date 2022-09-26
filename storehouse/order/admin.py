from django.contrib import admin
from django.contrib.admin import TabularInline

from order.models import Order, OrderItem, OrderItemBookItem


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 1


class OrderItemBookItemInline(TabularInline):
    model = OrderItemBookItem
    extra = 1
    readonly_fields = ['book_item_status']

    def book_item_status(self, orderitembookitem):
        return orderitembookitem.book_item.status


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_email', 'status', 'transaction_id']
    list_filter = ['id']
    inlines = [OrderItemInline]
    search_fields = ['transaction_id']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['book', 'order', 'quantity']
    list_filter = ['order']
    inlines = [OrderItemBookItemInline]
    search_fields = ['order']
