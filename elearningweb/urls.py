from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('courses/', views.CoursesView.as_view(), name='courses'),
    path('tests/', views.TestsView.as_view(), name='tests'),
    path('createtest/', views.CreateTestView.as_view(),name='createtest'),
    path('addquestions/', views.AddQuestionsView.as_view(),name='addquestions')
]