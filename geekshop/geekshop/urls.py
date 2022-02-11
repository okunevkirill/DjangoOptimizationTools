"""
geekshop URL Configuration
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('admins/', include('adminapp.urls', namespace='adminapp')),
    path('user/', include('authapp.urls', namespace='authapp')),
    path('baskets/', include('basketapp.urls', namespace='basketapp')),
    path('orders/', include('orderapp.urls', namespace='orderapp')),
    path('', include('mainapp.urls', namespace='mainapp')),

    path('', include('social_django.urls', namespace='social')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)), ]
