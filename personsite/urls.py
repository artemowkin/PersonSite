from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('auth/', include('accounts.urls')),

    # Local
    path('posts/', include('posts.urls')),
]

if __name__ == '__main__':
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
