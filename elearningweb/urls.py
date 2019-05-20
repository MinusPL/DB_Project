from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('courses/', views.CoursesView.as_view(), name='courses'),
    path('tests/<int:testID>', views.TestsView.as_view(), name='tests'),
    path('createtest/', views.CreateTestView.as_view(),name='createtest'),
    path('addquestions/<int:testID>', views.AddQuestionsView.as_view(),name='addquestions'),
    path('managetest/<int:testID>', views.ManageTestView.as_view(),name='managetest'),
    path('managetest/<int:questionID>/editquestion', views.EditQuestionView, name='editquestion')
]