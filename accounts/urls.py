from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('changepassword', views.changepassword, name='changepassword'),
    path('userdatachangeview', views.UserDataChangeView, name='userdatachange')
]
