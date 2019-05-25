from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('courses/', views.CoursesView.as_view(), name='courses'),
    path('courses/<int:pk>', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/<int:pk>/<int:class.id>', views.ClassesView.as_view(), name='class'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
 
]