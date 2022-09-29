from django.core.mail import send_mail


def order_status_email(transaction_id, status, email, value):
    email = email
    subject = f'Order status.'
    if value is None:
        message = f'You received this email because status of your oder with number {transaction_id} ' \
                  f'changed to {status}.'
    else:
        message = f'You received this email because status of your oder with number {transaction_id} ' \
                  f'changed from {value} to {status}.'
    from_email = 'admin@admin.admin'
    send_mail(subject, message, from_email, [email], fail_silently=False)
