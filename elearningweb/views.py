from django.shortcuts import render, redirect

from urllib.parse import urlencode
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.template import Context, Template
from django.http import HttpResponse

from django.views.generic import ListView, TemplateView, DetailView, FormView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin

from dbhandler.models import Course, CourseType, Module, Test, Answer, Question, Class, Instructor, Participant, CustomUser, TestResult
from .forms import QuestionForm, AnswerForm, AddCourseForm, AddClassForm

# Create your views here.

class CoursesView(ListView):
    model = Course
    template_name = 'courses.html'

class CourseDetailView(DetailView):
    model = Course
    template_name='course_detail.html'

class ClassesView(DetailView):
    model = Class
    def post(self, request, *args, **kwargs):
        comment = request.POST['comment'],
        author = request.POST['author'],
        id = request.POST['id']
        c=Comment(text=comment, author_id=author, class_id=id )
        c.save()
        return redirect('../class/%d' % c.id)            
    template_name = 'class.html'

class HomeView(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('user_courses')
        else:
            return render(request, 'index.html')

def completeTest(request,**kwargs):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    test=Test.objects.get(id=kwargs['testID'])
    classobj=Class.objects.get(id=test.class_id_id)
    try:
        Participant.objects.get(user_id_id=request.user.id,course_id_id=classobj.course_id_id)
    except Participant.DoesNotExist:
        if not request.user.has_perm('dbhandler.edit_course'):
            return render(request, 'permission_error.html')
    questionList = Question.objects.filter(test_id=kwargs['testID'])
    answerList = []
    for q in questionList:
        answerList.extend(Answer.objects.filter(question_id_id=q.id))
    c={
        'test':test,
        'questions':questionList,
        'answers':answerList,
        'qCount':questionList.count()
        }
    return render(request,"completeTest.html",c)

def finishView(request,**kwargs):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    test=Test.objects.get(id=kwargs['testID'])
    classobj=Class.objects.get(id=test.class_id_id)
    try:
        Participant.objects.get(user_id_id=request.user.id,course_id_id=classobj.course_id_id)
    except Participant.DoesNotExist:
        if not request.user.has_perm('dbhandler.edit_course'):
            return render(request, 'permission_error.html')
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
        score = 0
        for a in allAnsList:
            if a.id in ansList:
                if a.is_good == 1:
                    score = score + 1
        c={
            'checked':ansList,
            'test':test,
            'questions':questionsList,
            'answers':allAnsList,
            'score':score,
            'qCount':qCount
        }
        try:
            result = TestResult.objects.get(user=request.user.id,test=test.id)
            if result.result < score:
                result.result = score
            if result.maxScore < qCount:
                result.maxScore = qCount
            result.save()
        except TestResult.DoesNotExist:
            result = TestResult(user=request.user,test=test,result=score,maxScore=qCount)
            result.save()
    return render(request,"finishedTest.html",c)

def testScores(request,**kwargs):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    if not request.user.has_perm('dbhandler.edit_course'):
        return render(request, 'permission_error.html')
    test=Test.objects.get(id=kwargs['testID'])
    c={
        'test':test,
        'users':CustomUser.objects.all(),
        'results':TestResult.objects.filter(test=test)
        }
    return render(request,"testScores.html",c)

def createTest(request,**kwargs):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    if not request.user.has_perm('dbhandler.edit_course'):
        return render(request, 'permission_error.html')
    c={
        'classid':kwargs['classID']
        }
    if request.method == 'POST':
        testName = request.POST['testname']
        testDesc = request.POST['testdesc']
        ClassId = int(request.POST['cid'])
        t=Test(name=testName,description=testDesc,class_id_id=ClassId)
        t.save()
        return redirect('../../managetest/%d/addquestions' % t.id)
    return render(request,"createTest.html",c)

def addQuestions(request,**kwargs):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    if not request.user.has_perm('dbhandler.edit_course'):
        return render(request, 'permission_error.html')
    if request.method == 'POST':
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
    c = {
        'testID':kwargs['testID']
    }
    return render(request,"addQuestions.html",c)

def manageTest(request,**kwargs):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    if not request.user.has_perm('dbhandler.edit_course'):
        return render(request, 'permission_error.html')
    c={
        'test':Test.objects.get(id=kwargs['testID']),
        'questions':Question.objects.filter(test_id=kwargs['testID'])
        }
    if request.method == 'POST':
        tID = int(request.POST['tID'])
        toDelete = int(request.POST['qID'])
        Question.objects.filter(id=toDelete).delete()
        return redirect('../../managetest/%d' % tID)
    return render(request,"manageTest.html",c)


class LoginView(TemplateView):
    template_name = 'login.html'

class RegisterView(TemplateView):
    template_name = 'register.html'

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
            else:
                messages.error(request, 'Nieprawidłowe hasło do kursu')
    return render(request,'course_login.html')


def QuitCourse(request,kurs):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    if not request.user.has_perm('dbhandler.delete_participant'):
        return render(request, 'permission_error.html')
    k = Course.objects.filter(id=kurs).first()
    u=request.user
    if Instructor.objects.filter(course_id=k, user_id=u).exists():
        messages.error(request, 'Nie możesz zrezygnować z kursu którego jesteś prowadzącym')
    if Participant.objects.filter(course_id=k,user_id=u).exists():
        Participant.objects.filter(course_id=k, user_id=u).delete()
        messages.success(request, 'Nie należysz juz do kursu')
    return redirect('courses')

def UserCourses(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Musisz być zalogowany aby zobaczyć swoje kursy')
        return redirect('index')
    k=Course.objects.none()
    id_course_list=[]
    for p in Participant.objects.filter(user_id=request.user):
        id_course_list.append(p.course_id.id)
    for i in Instructor.objects.filter(user_id=request.user):
        if not i.course_id.id in id_course_list:
            id_course_list.append(i.course_id.id)
    k=Course.objects.filter(id__in=id_course_list)
    return render(request, 'user_courses.html', {'courses': k})

def UserDetailView(request):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    u=request.user
    groups=u.groups.all()
    return render(request, 'user_detail.html', {'groups': groups})
  
#Class
def AddClass(request):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    if not request.user.has_perm('dbhandler.add_class'):
        return render(request, 'class_error.html')
    f=AddClassForm(request.POST)
    if request.method == 'POST':
        classData=Class()
        classData.name = request.POST.get('name')
        classData.description = request.POST.get('description')
        classData.course_id = Course.objects.get(id=request.POST['course_id'])
        classData.save()
        return redirect('addclass')
    return render(request,'addclass.html',{'form': f})

def DeleteClass(request,classId):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    if not request.user.has_perm('dbhandler.delete_class'):
        return render(request, 'class_error.html')
    k = Class.objects.filter(id=classId)
    if k.exists():
        k.delete()
        return HttpResponse("Usunieto pomyslnie")
    return redirect('index')
