from django.urls import path
from . import views as v

app_name = 'store'


urlpatterns = [
    path('', v.items_view, name='items_view'),
    path('<slug:slug>/', v.item_detailed_view, name='item_detailed'),
    path('i<slug:slug>/', v.category_view, name='category_view'),
]