from django.urls import path
from . import views as v

app_name = 'cart'


urlpatterns = [
    path('', v.cart_view, name='cart_view'),
    path('add/', v.cart_add, name='add_to_cart',)
]