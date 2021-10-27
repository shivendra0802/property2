from django.urls import path
# from rest_framework import routers

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenVerifyView,
# )

from accounts import views
from accounts.views import signup, logout
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # auth endpoints 
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    # path('test',views.test,name='test'),

    # # user login
    path('front-user/login', views.FrontUserLoginTokenObtainPairView.as_view(), name='front_user_login'),
    path('admin/login', views.AdminLoginTokenObtainPairView.as_view(), name='admin_login'),
    path('supplier/login', views.SupplierLoginTokenObtainPairView.as_view(), name='supplier_login'),
    path('user/profile', views.UserProfileView.as_view(), name='user_profile'),

    # # jwt endpoints 
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('send', views.send_mail_to_all, name="sendmail"),
]

