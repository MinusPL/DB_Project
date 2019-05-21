from django.shortcuts import render, redirect
from django.template import Context, Template
from django.http import HttpResponse

from django.views.generic import ListView, TemplateView, DetailView, FormView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin
from dbhandler.models import Course, Test, Answer, Question, Class
from .forms import QuestionForm, AnswerForm

# Create your views here.

class CoursesView(ListView):
    model = Course
    template_name = 'courses.html'
    #login_url = "/elearning/login/"
    #redirect_field_name = "redirect_to"

class CourseDetailView(DetailView):
	model = Course
	template_name = 'course_detail.html'

class HomeView(TemplateView):
    template_name = 'index.html'

class TestsView(TemplateView):
    model = Test
    def get_context_data(self, **kwargs):
        context = super(TestsView, self).get_context_data(**kwargs)
        context['test'] = Test.objects.get(id=kwargs['testID'])
        context['questions'] = Question.objects.filter(test_id=kwargs['testID'])
        answerList = []
        for q in Question.objects.filter(test_id=kwargs['testID']):
            answerList.extend(Answer.objects.filter(question_id_id=q.id))
        context['answers'] = answerList
        context['qCount'] = Question.objects.filter(test_id=kwargs['testID']).count()
        return context
    template_name = 'tests.html'

def FinishView(request,**kwargs):
    if request.method == 'POST':
        qCount=int(request.POST['qc'])
        ansList=[]
        questionsList=Question.objects.filter(test_id=kwargs['testID'])
        allAnsList=[]
        for q in questionsList:
            allAnsList.extend(Answer.objects.filter(question_id_id=q.id))
        for i in range(1,qCount+1):
            ch=int(request.POST['Question%d' % i])
            ansList.append(ch)
        c={
            'checked':ansList,
            'test':Test.objects.get(id=kwargs['testID']),
            'questions':questionsList,
            'answers':allAnsList
        }
    return render(request,"finishedTest.html",c)
             

        
class CreateTestView(TemplateView):
    template_name = 'createTest.html'
    def get_context_data(self, **kwargs):
        context = super(CreateTestView, self).get_context_data(**kwargs)
        context['classid'] = Class.objects.get(id=kwargs['classID'])
        return context
    def post(self, request, *args, **kwargs):
        testName = request.POST['testname']
        testDesc = request.POST['testdesc']
        ClassId = int(request.POST['cid'])
        t=Test(name=testName,description=testDesc,class_id_id=ClassId)
        t.save()
        return redirect('../addquestions/%d' % t.id)

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
        testID = request.POST['testid']
        q=Question(question_text=qText,test_id_id=testID)
        q.save()
        i = 1
        for a in ans:
            if i == int(corAns):
                a=Answer(answer_text=a,is_good=1,question_id_id=q.id)
            else:
                a=Answer(answer_text=a,is_good=0,question_id_id=q.id)
            a.save()
            i = i+1
        return redirect('addquestions',testID=testID)

class ManageTestView(TemplateView):
    template_name = 'manageTest.html'
    def get_context_data(self, **kwargs):
        context = super(ManageTestView, self).get_context_data(**kwargs)
        context['test'] = Test.objects.get(id=kwargs['testID'])
        context['questions'] = Question.objects.filter(test_id=kwargs['testID'])
        return context
    def post(self, request, *args, **kwargs):
        tID = int(request.POST['tID'])
        toDelete = int(request.POST['qID'])
        Question.objects.filter(id=toDelete).delete()
        return redirect('../managetest/%d' % tID)

class LoginView(TemplateView):
    template_name = 'login.html'

class RegisterView(TemplateView):
    template_name = 'register.html'
