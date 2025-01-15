from django.urls import path
from . import views as v

app_name = 'store'


urlpatterns = [
    path('', v.items_view, name='items'),
    path('item/<slug:slug>/', v.item_detail_view, name='item_detail'),
    path('<slug:slug>/', v.category_view, name='category_list'),
    path('search', v.search, name='search'), # TODO to replace with an actual search functionality
]