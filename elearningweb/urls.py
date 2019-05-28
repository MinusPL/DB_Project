from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('courses/', views.CoursesView.as_view(), name='courses'),
    path('class/completetest/<int:testID>', views.completeTest, name='completetest'),
    path('class/completetest/<int:testID>/finished', views.finishView, name='finished'),
    path('class/<int:classID>/createtest', views.createTest, name='createtest'),
    path('managetest/<int:testID>/', views.manageTest,name='managetest'),
    path('managetest/<int:testID>/addquestions', views.addQuestions, name='addquestions'),
    path('courses/<int:pk>', views.CourseDetailView.as_view(), name='course_detail'),
    path('class/<int:pk>', views.ClassesView.as_view(), name='class'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('courses/<int:pk>', views.CourseDetailView.as_view(), name='course_detail'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('courses/add/', views.AddCourse, name='addcourse'),
    path('courses/join/<int:kurs>',views.JoinCourse,name='join_course'),
    path('courses/quit/<int:kurs>',views.QuitCourse,name='quit_course'),
    path('user_courses', views.UserCourses, name ='user_courses'),
    path('courses/testscores/<int:testID>',views.testScores,name='testscores'),
    path('class/add/', views.AddClass, name='addclass'),
    path('class/delete/<int:classId>',views.DeleteClass,name='delete_class'),
    path('user_courses', views.UserCourses, name ='user_courses'),
    path('userdetailview', views.UserDetailView, name='userdetailview')
]