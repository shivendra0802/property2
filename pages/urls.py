from django.urls import path ,include  

from . import views 

urlpatterns = [
    path('Account/',include('accounts.urls')),
    path('', views.index, name='index'),
    path('dashbord',views.index, name='dashbord'),
    path('about', views.about, name='about'),
    path('login',views.login,name="login"),
    path('register',views.register,name="register"),
    
    path('single',views.single,name="login"),
]