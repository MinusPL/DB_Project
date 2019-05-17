from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dbhandler.models import Course, Test, Answer, Question, Class

# Create your views here.

class CoursesView(ListView):
    model = Course
    template_name = 'courses.html'
    #login_url = "/elearning/login/"
    #redirect_field_name = "redirect_to"

class HomeView(TemplateView):
    template_name = 'index.html'

class TestsView(ListView):
    def get_context_data(self, **kwargs):
        context = super(TestsView, self).get_context_data(**kwargs)
        context['questions'] = Question.objects.all()
        context['answers'] = Answer.objects.all()
        return context
    template_name = 'tests.html'
        
class CreateTestView(TemplateView):
    model = Class
    template_name = 'createTest.html'
    def post(self, request, *args, **kwargs):
        testName = request.POST['testname']
        testDesc = request.POST['testdesc']
        #ClassId = request.POST['classid']
        t=Test(name=testName,description=testDesc,class_id_id=2)
        t.save()
        return redirect('addQuestions')

class AddQuestionsView(TemplateView):
    template_name = 'addQuestions.html'
    def post(self, request, *args, **kwargs):
        qText = request.POST['content']
        ans = [
            request.POST['answer1'],
            request.POST['answer2'],
            request.POST['answer3'],
            request.POST['answer4']
        ]
        corAns = request.POST['isCorrect']
        #ClassId = request.POST['classid']
        q=Question(question_text=qText,test_id_id=5)
        q.save()
        i = 1
        for a in ans:
            if i==corAns:
                a=Answer(answer_text=a,is_good=1,question_id_id=q.id)
            else:
                a=Answer(answer_text=a,is_good=0,question_id_id=q.id)
            a.save()
            i = i+1
        return redirect('addquestions')

class ManageTestView(TemplateView):
    template_name = 'manageTest.html'
    def get_context_data(self, **kwargs):
        context = super(TestsView, self).get_context_data(**kwargs)
        context['questions'] = Question.objects.all()
        context['answers'] = Answer.objects.all()
        return context
 #   def post(self, request, *args, **kwargs):