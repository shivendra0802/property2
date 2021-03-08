from django.urls import path,include

from . import views
from rest_framework import routers
#
router = routers.DefaultRouter()
router.register('owaish', views.ListingView)

urlpatterns = [
    path('a/', include(router.urls)),
    path('sidd', views.ListingView, name='listings'),
    path('<int:listing_id>', views.listing, name='listing'),
    path('search', views.search, name='search')
]