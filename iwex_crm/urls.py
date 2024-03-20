from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.conf.urls.static import static
from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path
from rest_framework import permissions

from .views import main_page
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)





from django.views.i18n import set_language


urlpatterns = [
#     path("i18n/", include("django.conf.urls.i18n")),
    path('admin/', admin.site.urls),
    path('', main_page, name='main-page'),
    path('i18n/', set_language, name='set_language'),
    path('chaining/', include('smart_selects.urls')),
    path('accounts/', include('applications.accounts.urls')),
    path('core/', include('applications.core.urls')),
    path('staff/', include('applications.staff.urls')),
    
    # path('common/', include('applications.common.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# handler404 = error_404_page
# handler500 = error_500_page

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
                   static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
