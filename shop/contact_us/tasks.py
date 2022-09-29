from django.core.mail import send_mail


def contactus(subject, message, from_email):
    email = 'ad@ad.ad'  # Administration email
    subject = subject
    message = message
    send_mail(subject, message, from_email, [email], fail_silently=False)
