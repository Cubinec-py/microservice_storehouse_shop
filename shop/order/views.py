from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

import json
import datetime

from order.utils import cartData, guestOrder
from order.forms import OrderForm
from order.models import Book, Order, OrderItem, ShippingAddress, Customer


def cart(request):
	data = cartData(request)

	order = data['order']
	items = data['items']

	context = {'items': items, 'order': order}
	return render(request, 'order/cart.html', context)


def checkout(request):
	data = cartData(request)
	order = data['order']
	items = data['items']

	context = {'items': items, 'order': order}
	return render(request, 'order/checkout.html', context)


def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	customer = request.user
	product = Book.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, book=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)
	elif action == 'delete':
		orderItem.quantity = 0

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)


def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

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
		else:
			ShippingAddress.objects.create(
				guest=customer,
				order=order,
				address=data['shipping']['address'],
				city=data['shipping']['city'],
				state=data['shipping']['state'],
				zipcode=data['shipping']['zipcode'],
			)

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
