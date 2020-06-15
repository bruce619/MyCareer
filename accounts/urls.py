from django.urls import path
from .views import *
from accounts import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('profile/', user_views.profile, name='profile'),


]
#  Saves static files in static folder
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#  Saves media files in media folder
if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
