from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('courses/', views.CoursesView.as_view(), name='courses'),
    path('tests/<int:testID>', views.TestsView.as_view(), name='tests'),
    path('tests/<int:testID>/finished', views.FinishView, name='finished'),
    path('createtest/<int:classID>', views.CreateTestView.as_view(),name='createtest'),
    path('addquestions/<int:testID>', views.AddQuestionsView.as_view(),name='addquestions'),
    path('managetest/<int:testID>', views.ManageTestView.as_view(),name='managetest'),
    path('courses/<int:pk>', views.CourseDetailView.as_view(), name='course_detail'),
    path('class/<int:pk>', views.ClassesView.as_view(), name='class'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('courses/<int:pk>', views.CourseDetailView.as_view(), name='course_detail'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('courses/add/', views.AddCourse, name='addcourse'),
    path('courses/join/<int:kurs>',views.JoinCourse,name='join_course'),
    path('courses/quit/<int:kurs>',views.QuitCourse,name='quit_course'),
    path('user_courses', views.UserCourses, name ='user_courses')
]