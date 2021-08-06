from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),

    # Documentation
    path('docs/', TemplateView.as_view(
        template_name='redoc.html',
    ), name='redoc'),

    # Authentication
    path('auth/', include('accounts.urls')),

    # Local
    path('posts/', include('posts.urls')),
    path('shop/products/', include('shop.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
