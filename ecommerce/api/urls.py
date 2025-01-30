from django.urls import path, include
from drf_yasg import openapi
from . import views as v

app_name = 'api'


urlpatterns = [
    path('items', v.ItemsApiView.as_view(), name='api_items'),
    path('items/<int:pk>/', v.ItemDetailAPIView.as_view()),

    # Reviews
    path('reviews/create/', v.ReviewCreateView.as_view()),

    # User
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]