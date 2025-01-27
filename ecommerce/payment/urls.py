from django.urls import path
from .webhooks import stripe_webhook

from . import views as v

app_name = 'payment'

urlpatterns = [
    path('payment-success/', v.payment_success, name='payment_success'),
    path('payment-failure/', v.payment_failure, name='payment_failure'),
    path('shipping/', v.shipping, name='shipping'),
    path('checkout/', v.checkout, name='checkout'),
    path('complete-order/', v.complete_order, name='complete_order'),

    # stripe webhook
    path('webhook-stripe/', stripe_webhook, name='stripe_webhook'), # activated for testing usign stripe listen --forward-to localhost:8000/payment/webhook-stripe/

    #admin paths
    path("order/<int:order_id>/pdf", v.admin_order_pdf, name='admin_order_pdf'),

]
# to add: order_detail