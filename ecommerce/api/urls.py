from django.urls import path
from drf_yasg import openapi
from . import views as v

app_name = 'api'


urlpatterns = [
    path('items', v.ItemsApiView.as_view(), name='api_items'),
    
    
]