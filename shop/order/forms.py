from django import forms
from django.core.exceptions import ValidationError

from order.models import Customer


def validate_name_exists(value):
    incident = Customer.objects.filter(name=value)
    if not incident:
        raise ValidationError('No such name in orders')


def validate_email_exists(value):
    incident = Customer.objects.filter(email=value)
    if not incident:
        raise ValidationError('No such email in orders')


class OrderForm(forms.Form):

    name = forms.CharField(max_length=50, required=True, validators=[validate_name_exists])
    email = forms.EmailField(max_length=50, required=True, validators=[validate_email_exists])
