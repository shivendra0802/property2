from django.urls import path,include

from . import views
from rest_framework import routers
#
router = routers.DefaultRouter()
router.register('view', views.RealtorsView)

urlpatterns = [
    path('r/', include(router.urls)),
]