from django.shortcuts import render
from django.http import JsonResponse

import json
import datetime

from order.utils import cart_data, guest_order
from order.forms import OrderForm
from order.models import Book, Order, OrderItem, ShippingAddress, Customer
from order.tasks import order_to_storehouse, check_order_status, confirm_order_email


def cart(request):
	data = cart_data(request)

	order = data['order']
	items = data['items']

	context = {'items': items, 'order': order}
	return render(request, 'order/cart.html', context)


def checkout(request):
	data = cart_data(request)
	order = data['order']
	items = data['items']

	context = {'items': items, 'order': order}
	return render(request, 'order/checkout.html', context)


def update_item(request):
	data = json.loads(request.body)
	product_id = data['productId']
	action = data['action']

	customer = request.user
	product = Book.objects.get(id=product_id)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	order_item, created = OrderItem.objects.get_or_create(order=order, book=product)

	if action == 'add':
		if order_item.quantity < product.count:
			order_item.quantity = (order_item.quantity + 1)
		else:
			order_item.quantity = order_item.quantity
	elif action == 'remove':
		order_item.quantity = (order_item.quantity - 1)
	elif action == 'delete':
		order_item.quantity = 0

	order_item.save()

	if order_item.quantity <= 0:
		order_item.delete()

	return JsonResponse('Item was added', safe=False)


def process_order(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guest_order(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping is True:
		if request.user.is_authenticated:
			ShippingAddress.objects.create(
				customer=customer,
				order=order,
				address=data['shipping']['address'],
				city=data['shipping']['city'],
				state=data['shipping']['state'],
				zipcode=data['shipping']['zipcode'],
			)
			customer_email = request.user.email
			customer_name = request.user.username
			order_to_storehouse.delay(customer_email, transaction_id)
			confirm_order_email(customer_email, transaction_id, customer_name)
		else:
			ShippingAddress.objects.create(
				guest=customer,
				order=order,
				address=data['shipping']['address'],
				city=data['shipping']['city'],
				state=data['shipping']['state'],
				zipcode=data['shipping']['zipcode'],
			)
			customer_email = customer.email
			customer_name = customer.name
			order_to_storehouse.delay(customer_email, transaction_id)
			confirm_order_email(customer_email, transaction_id, customer_name)

	return JsonResponse('', safe=False)


def order_view(request):

	if request.user.is_authenticated:
		order = Order.objects.filter(customer=request.user)
		for item in order:
			order_id = item.id
			check_order_status.delay(order_id)
		context = {
			'order_list': order
		}
		return render(request, 'order/order_list.html', context)

	else:
		if 'submit' in request.GET:
			form = OrderForm(request.GET)
			if form.is_valid():
				transaction_id = form.cleaned_data["order_number"]
				if Order.objects.filter(transaction_id=transaction_id) is not None:
					order = Order.objects.filter(transaction_id=transaction_id)
					for item in order:
						order_id = item.id
						check_order_status.delay(order_id)
					guest_context = {'form': form, 'order_list': order}
					return render(request, 'order/order_list.html', guest_context)
		else:
			form = OrderForm()
		order = None
		guest_context = {'form': form, 'order_list': order}
		return render(request, 'order/order_list.html', guest_context)


def order_detail(request, pk):
	order = OrderItem.objects.filter(order=pk)
	context = {'object_list': order}
	return render(request, 'order/order_detail.html', context)
