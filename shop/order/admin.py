from django.contrib import admin

from order.models import Order


@admin.register(Order)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['customer', 'guest', 'complete']
