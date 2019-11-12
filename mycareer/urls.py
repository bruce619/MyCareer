from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('nueoffshore.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('api/', include([
        path('', include('nueoffshore.api.urls')),
    ])),
]
if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = 'nueoffshore.views.home.handler404'
# handler500 = 'nueoffshore.views.home.handler500'
