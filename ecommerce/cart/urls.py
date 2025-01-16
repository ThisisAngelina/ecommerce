from django.urls import path
from . import views as v

app_name = 'cart'


urlpatterns = [
    path('', v.cart_view, name='cart_view'),
    path('add', v.cart_add, name='add_to_cart'),
    path('delete', v.cart_delete, name='delete_from_cart'),
    path('update', v.cart_update, name='update_cart'),
]