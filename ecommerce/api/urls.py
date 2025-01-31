from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from . import views as v

app_name = 'api'

schema_view = get_schema_view(
    openapi.Info(
        title="ReFRESH api",
        default_version="v1",
        description="ReFRESH api to GET item details and POST item reviews",
        terms_of_service="",
        contact=openapi.Contact(email="angelina.chigrinetc.dev@gmail.com"),
        license=openapi.License(name=""),
    ),
    public=True,
)

urlpatterns = [
    path('items', v.ItemsApiView.as_view(), name='api_items'),
    path('items/<int:pk>/', v.ItemDetailAPIView.as_view()),

    # Reviews
    path('reviews/create/', v.ReviewCreateView.as_view()),

    # User
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    # Documentation
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]