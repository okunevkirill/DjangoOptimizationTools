"""geekshop URL Configuration"""

from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('authapp.urls', namespace='authapp')),
    path('baskets/', include('baskets.urls', namespace='baskets')),
    path('admins/', include('admins.urls', namespace='admins')),
    path('', include('mainapp.urls', namespace='mainapp')),

    url(r'^i18n/', include('django.conf.urls.i18n')),
    path('', include('social_django.urls', namespace='social')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
