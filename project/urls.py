from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings
from django.urls import re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="SimotapLike API",
        default_version="v1",
        description="SimotapLike",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email=settings.DEVELOPER_EMAIL),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('cards.urls')),
    path('api/v1/auth/', include('accounts.urls')),
    # path('api/auth/', include('dj_rest_auth.urls')), 
    # path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
