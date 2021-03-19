from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views
from django.conf.urls import url


urlpatterns = [
    path('', include('pages.urls')),
     path('listings/', include('listings.urls')),
     path('accounts/', include('accounts.urls')),
     path('realtorss/', include('realtors.urls')),
     path('admin/', admin.site.urls),
     path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
  
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
