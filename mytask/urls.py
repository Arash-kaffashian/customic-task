from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('mockups.urls')),
    path('admin/', admin.site.urls),
]

# WITH THIS CONFIG YOU CAN READ FILES LIKE IMAGES IN BROWSER WHILE THE DEBUG IS TRUE
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
