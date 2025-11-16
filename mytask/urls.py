from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# green code : what is swagger ?
urlpatterns = [
    path('', include('mockups.urls')),
]

# red code : is it necessary to be in setting.py at gitignore ?
# WITH THIS CONFIG YOU CAN READ FILES LIKE IMAGES IN BROWSER WHILE THE DEBUG IS TRUE
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
