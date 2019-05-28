from django.shortcuts import render, redirect

from urllib.parse import urlencode
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template import Context, Template
from django.http import HttpResponse
from django.contrib import messages
from django.views.generic import ListView, TemplateView, DetailView, FormView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin

from dbhandler.models import Course, CourseType, Module, Test, Answer, Question, Class, Instructor, Participant, CustomUser
from .forms import QuestionForm, AnswerForm, AddCourseForm

# Create your views here.

class CoursesView(ListView):
    model = Course
    template_name = 'courses.html'

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

def UserDetailView(request):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    u=request.user
    groups=u.groups.all()
    return render(request, 'user_detail.html', {'groups': groups})


def AddCourse(request):
    #if not Instructor.objects.filter(user_id=request.user.id):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    if not request.user.has_perm('dbhandler.add_course'):
        return render(request, 'permission_error.html')

    f=AddCourseForm(request.POST)
    if request.method=='POST':
        course=Course()
        course.name=request.POST['name']
        if Course.objects.filter(name=course.name).exists():
            messages.error(request, 'Istnieje już kurs o tej nazwie')
            return redirect('addcourse')
        course.course_type = CourseType.objects.get(id=request.POST['course_type'])
        course.module_id = Module.objects.get(id=request.POST['module_id'])
        course.description= request.POST['description']
        course.password=request.POST['password']
        course.save()
        instr = Instructor()
        instr.course_id = course
        instr.user_id = request.user
        instr.save()
        return redirect('courses')
    return render(request,'addcourse.html',{'form': f})

def JoinCourse(request,kurs):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    if not request.user.has_perm('dbhandler.add_participant'):
        return render(request, 'permission_error.html')
    course=Course.objects.get(id=kurs)
    user=request.user
    if Participant.objects.filter(course_id=course,user_id=user).exists() or Instructor.objects.filter(course_id=course,user_id=user).exists() :
        return redirect('course_detail', course.pk)
    else:
        if request.method=='POST':
            password=request.POST['coursepass']
            if password==course.password:
                participant=Participant()
                participant.course_id=course
                participant.user_id=user
                participant.save()
                return redirect('course_detail',course.pk)
    return render(request,'course_login.html')


def QuitCourse(request,kurs):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    if not request.user.has_perm('dbhandler.delete_participant'):
        return render(request, 'permission_error.html')
    k = Course.objects.filter(id=kurs).first()
    u=request.user
    if Participant.objects.filter(course_id=k,user_id=u).exists():
        Participant.objects.filter(course_id=k, user_id=u).delete()
        messages.success(request, 'Nie należysz juz do kursu')
    return redirect('courses')

def UserCourses(request):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    k=Course.objects.none()
    id_course_list=[]
    for p in Participant.objects.filter(user_id=request.user):
        id_course_list.append(p.course_id.id)
    for i in Instructor.objects.filter(user_id=request.user):
        if not i.course_id.id in id_course_list:
            id_course_list.append(i.course_id.id)
    k=Course.objects.filter(id__in=id_course_list)
    return render(request, 'user_courses.html', {'courses': k})

