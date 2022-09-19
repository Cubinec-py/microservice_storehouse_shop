import json
from order.models import Order, OrderItem, Customer
from books.models import Book


def cookieCart(request):

	# Create empty cart for now for non-logged in user
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}
		print('CART:', cart)

	items = []
	order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}

	for i in cart:
		# We use try block to prevent items in cart that may have been removed from causing error
		try:
			if (cart[i]['quantity'] > 0):

				product = Book.objects.get(id=i)
				total = (product.price * cart[i]['quantity'])

				order['get_cart_total'] += total
				order['get_cart_items'] += cart[i]['quantity']

				item = {
					'id': product.id,
					'book': {
						'id': product.id,
						'title': product.title,
						'price': product.price,
						'imageURL': product.image.url
					},
					'quantity': cart[i]['quantity'],
					'digital': product.digital, 'get_total': total,
				}
				items.append(item)

				if product.digital is False:
					order['shipping'] = True
		except:
			pass

	return {'order': order, 'items': items}


def cartData(request):
	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
	else:
		cookieData = cookieCart(request)
		order = cookieData['order']
		items = cookieData['items']

	return {'order': order, 'items': items}


def guestOrder(request, data):
	name = data['form']['name']
	email = data['form']['email']

	cookieData = cookieCart(request)
	items = cookieData['items']

	customer, created = Customer.objects.get_or_create(
			email=email,
			)
	customer.name = name
	customer.save()

	order = Order.objects.create(
		guest=customer,
		complete=False,
		)

	for item in items:
		product = Book.objects.get(id=item['id'])
		orderItem = OrderItem.objects.create(
			book=product,
			order=order,
			quantity=(item['quantity'] if item['quantity'] > 0 else -1 * item['quantity']),
		)
	return customer, order
