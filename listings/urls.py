from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from rest_framework import routers
from .views import ManageListingView
#
# router = routers.DefaultRouter()
# router.register('view', views.ListingView)

urlpatterns = [
    # path('r/', include(router.urls)),
    path('listing', views.ListingView, name='listings'),
    path('<int:listing_id>', views.listing, name='listing'),
    path('search', views.search, name='search'),
    path('displaydata',views.displaydata, name="view"),
    path('managelisting', views.ManageListingView, name='managelistings')
]
