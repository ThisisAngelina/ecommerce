from django.urls import path
from . import views as v

app_name = 'store'


urlpatterns = [
    path('', v.ItemsListView.as_view(), name='items'),
    path('item/<slug:slug>/', v.item_detail_view, name='item_detail'),
    path('category/<slug:slug>/', v.category_view, name='category_list'),
    path('search', v.search, name='search'), 
]