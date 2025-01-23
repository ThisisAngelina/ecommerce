from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import Order, ShippingAddress


@shared_task()
def send_order_confirmation(order_id):
    
    order = Order.objects.get(id=order_id)
    subject = f'Your {settings.PROJECT_NAME}  order is on its way!'
    receipent_email = ShippingAddress.objects.get(user=order.user).email
    message = f'Your order is on its way. Your order number is {order.id}.'

    mail_to_sender = send_mail(
        subject,message=message,from_email=settings.EMAIL_HOST_USER, recipient_list=[receipent_email],
    )
    print('email was handled with celery')
    return mail_to_sender