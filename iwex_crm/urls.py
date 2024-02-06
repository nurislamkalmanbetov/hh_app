from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.conf.urls.static import static
from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg2.views import get_schema_view
from .views import main_page

from drf_yasg2 import openapi




from django.views.i18n import set_language


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    # url='https://crm.iwex.kg',
)

urlpatterns = [
#     path("i18n/", include("django.conf.urls.i18n")),
    path('admin/', admin.site.urls),
    path('', main_page, name='main-page'),
    path('i18n/', set_language, name='set_language'),
    path('chaining/', include('smart_selects.urls')),
    path('accounts/', include('applications.accounts.urls')),
    path('core/', include('applications.core.urls')),
    # path('common/', include('applications.common.urls')),
    # path('bot/', include('applications.bot.urls')),
     re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
     path(
          "swagger/",
          schema_view.with_ui("swagger", cache_timeout=0),
          name="schema-swagger-ui",
     ),
     path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# handler404 = error_404_page
# handler500 = error_500_page

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
#                    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
