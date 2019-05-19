from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('courses/', views.CoursesView.as_view(), name='courses'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('courses/<int:pk>', views.CourseDetailView.as_view(), name='course_detail'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('courses/add/', views.AddCourse, name='addcourse'),
    path('courses/join/<int:kurs>',views.JoinCourse,name='join_course'),
    path('courses/quit/<int:kurs>',views.QuitCourse,name='quit_course'),

]