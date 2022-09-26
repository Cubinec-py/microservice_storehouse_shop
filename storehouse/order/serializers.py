from rest_framework import serializers

from order.models import Order, OrderItem, ShippingAddress


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['book', 'quantity', 'order']


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['customer_email', 'transaction_id', 'date_ordered']


class ShippingAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShippingAddress
        fields = ['order', 'address', 'city', 'state', 'zipcode']
