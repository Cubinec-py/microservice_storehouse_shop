from django.urls import path

from . import views

urlpatterns = [
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

	path('order_info/', views.order_view, name='order_info'),
	path('order_info/detail/<pk>', views.order_detail, name='order_detail')
]
