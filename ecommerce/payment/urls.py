from django.urls import path

from . import views as v

urlpatterns = [
    path('payment-success/', v.payment_success, name='payment-success'),
    path('payment-failure/', v.payment_failure, name='payment-failure'),
    path('shipping/', v.shipping, name='shipping'),
    path('checkout/', v.checkout, name='checkout'),
    path('complete-order/', v.complete_order, name='complete-order'),

]
# to add: order_detail