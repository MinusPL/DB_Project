from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('changepassword', views.changepassword, name='changepassword'),
    path('userdatachangeview', views.UserDataChangeView, name='userdatachange'),
    path('password_reset', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
