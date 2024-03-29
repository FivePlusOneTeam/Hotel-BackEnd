from django.contrib import admin
from django.urls import path,include
from .settings import admin_url
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static


schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API Documentation for hotel",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="FivePlusOne.ir@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)





urlpatterns = [
    path(f'admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/', include('rooms.urls')),
    path('api/', include('food.urls')),
    path('api/', include('reports.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]





if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



