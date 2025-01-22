from django.urls import path

from . import views as v

app_name = 'payment'

urlpatterns = [
    path('payment-success/', v.payment_success, name='payment_success'),
    path('payment-failure/', v.payment_failure, name='payment_failure'),
    path('shipping/', v.shipping, name='shipping'),
    path('checkout/', v.checkout, name='checkout'),
    path('complete-order/', v.complete_order, name='complete_order'),

]
# to add: order_detail