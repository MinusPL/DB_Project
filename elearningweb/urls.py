from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('courses/<int:page>', views.CoursesView, name='courses'),
    path('class/completetest/<int:testID>', views.completeTest, name='completetest'),
    path('class/completetest/<int:testID>/finished', views.finishView, name='finished'),
    path('class/<int:classID>/createtest', views.createTest, name='createtest'),
    path('managetest/<int:testID>/', views.manageTest,name='managetest'),
    path('managetest/<int:testID>/addquestions', views.addQuestions, name='addquestions'),
    path('managetest/<int:testID>/editquestion/<int:questionID>', views.editQuestion, name='editquestion'),
    path('class/<int:pk>', views.ClassesView, name='class'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('course/<int:pk>', views.CourseDetailView.as_view(), name='course_detail'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('course/add/', views.AddCourse, name='addcourse'),
    path('course/join/<int:kurs>',views.JoinCourse,name='join_course'),
    path('course/quit/<int:kurs>',views.QuitCourse,name='quit_course'),
    path('course/edit/<int:kurs>',views.EditCourse,name='edit_course'),
    path('user_courses', views.UserCourses, name ='user_courses'),
    path('courses/testscores/<int:testID>',views.testScores,name='testscores'),
    path('class/add/', views.AddClass, name='addclass'),
    path('class/delete/<int:classId>',views.DeleteClass,name='delete_class'),
    path('user_courses/<int:page>', views.UserCourses, name ='user_courses'),
    path('course/addinstr/<int:kurs>', views.AddCourseInstructor, name ='add_instr'),
    path('userdetailview', views.UserDetailView, name='userdetailview'),
    path('class/edit/<int:classId>',views.EditClass,name='edit_class'),
]