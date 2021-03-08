from django.urls import path,include

from . import views
from rest_framework import routers
#
router = routers.DefaultRouter()
router.register('sidd', views.RealtorsView)

urlpatterns = [
    path('b/', include(router.urls)),
]