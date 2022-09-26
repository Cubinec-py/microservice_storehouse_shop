from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

import json
import datetime

from order.utils import cart_data, guest_order
from order.forms import OrderForm
from order.models import Book, Order, OrderItem, ShippingAddress, Customer
from order.tasks import order_to_storehouse


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
		order_item.quantity = (order_item.quantity + 1)
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
			# order_to_storehouse(customer, transaction_id)
		else:
			ShippingAddress.objects.create(
				guest=customer,
				order=order,
				address=data['shipping']['address'],
				city=data['shipping']['city'],
				state=data['shipping']['state'],
				zipcode=data['shipping']['zipcode'],
			)
			# order_to_storehouse(customer, transaction_id)

	return JsonResponse('', safe=False)


def order_view(request):

	if request.user.is_authenticated:
		order = Order.objects.filter(customer=request.user)
		context = {
			'order_list': order
		}
		return render(request, 'order/order_list.html', context)

	else:
		if 'submit' in request.POST:
			form = OrderForm(request.POST)
			if form.is_valid():
				name = form.cleaned_data["name"]
				email = form.cleaned_data["email"]
				if Customer.objects.filter(name=name, email=email) is not None:
					guest = get_object_or_404(Customer, name=name, email=email)
					order = Order.objects.filter(guest=guest.id)
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
