from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django_email_verification import urls as email_urls


urlpatterns = [
    path('', include('store.urls')),  
    path('admin/', admin.site.urls), 
    path('cart/', include('cart.urls')),
    path('account/', include('account.urls')),
    path('email/', include(email_urls), name='verify_email'),
    path('payment/', include('payment.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),  # include the Debug Toolbar
    ]
    # Serve static and media files during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
