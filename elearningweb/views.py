from django.shortcuts import render, redirect

from urllib.parse import urlencode
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.template import Context, Template
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime

from django.views.generic import ListView, TemplateView, DetailView, FormView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin

from dbhandler.models import *
from .forms import *

# Create your views here.


def CoursesView(request,**kwargs):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    fname=''
    lname=''
    cname=''
    mname=''
    instructors = Instructor.objects.all().order_by('pk')
    if 'course_name' in request.GET:
        if request.GET['course_name'] is not '':
            cname=request.GET['course_name']
            instructors=instructors.filter(course_id__name__contains=cname)
    if 'instr_name' in request.GET:
        if request.GET['instr_name'] is not '':
            fname=request.GET['instr_name']
            instructors=instructors.filter(user_id__first_name__contains=fname)
    if 'instr_lastname' in request.GET:
        if request.GET['instr_lastname'] is not '':
            lname=request.GET['instr_lastname']
            instructors=instructors.filter(user_id__last_name__contains=lname)
    if 'module_name' in request.GET:
        if request.GET['module_name'] is not '':
            mname=request.GET['module_name']
            instructors=instructors.filter(course_id__module_id__name__contains=mname)
    search_query = '?course_name='+cname+'&instr_name='+fname+'&instr_lastname'+lname+'&module_name='+mname

    page = kwargs['page']

    paginator = Paginator(instructors, 10)
    try:
        instructors = paginator.page(page)
    except PageNotAnInteger:
        instructors = paginator.page(1)
    except EmptyPage:
        instructors = paginator.page(paginator.num_pages)
    c = {
        'search_query':search_query,
        'instructors':instructors,
    }

    return render(request,"courses.html",c)

#TO-DO: NAPRAWIC WYSZUKIWANIE
# class CoursesView(ListView):
#     model = Course
#     template_name = 'courses.html'
#     def get_queryset(self):
#         result = super(CoursesView, self).get_queryset()
#         query = self.request.GET.get('search')
#         if query:
#              result = result.filter(
#                     name__icontains=query
#             )
        


class CourseDetailView(DetailView):
    model = Course
    template_name='course_detail.html'

def ClassesView(request,**kwargs):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')

    k = Class.objects.get(pk=kwargs['pk'])
    if not (Participant.objects.filter(course_id=k.course_id,user_id=request.user).exists() or Instructor.objects.filter(course_id=k.course_id,user_id=request.user).exists()):
        if not request.user.has_perm('dbhandler.view_class'):
            return render(request, 'permission_error.html')   

    if request.method == 'POST':
        comment = request.POST['comment']
        author = int(request.POST['author']) 
        cid = int(request.POST['id'])
        c=Comment(text=comment, author_id=request.user, class_id=Class.objects.get(id=cid))
        c.save()
        return redirect('class', kwargs['pk']) 

    cont = Content.objects.get(class_id=k, valid_until__isnull=True)

    c = {
        'class': k,
        'content':cont
    }
    
    return render(request, 'class.html', c)          


# class ClassesView(DetailView):
#     model = Class
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         k = Class.objects.get(pk=self.kwargs['pk'])
#         context['content'] = Content.objects.get(class_id=k, valid_until__isnull=True)
#         return context
#     def post(self, request, *args, **kwargs):
#         comment = request.POST['comment']
#         author = int(request.POST['author']) 
#         cid = int(request.POST['id'])
#         c=Comment(text=comment, author_id=request.user, class_id=Class.objects.get(id=cid))
#         c.save()
#         return redirect('class', kwargs['pk'])            
#     template_name = 'class.html'


class HomeView(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('user_courses', 1)
        else:
            return render(request, 'index.html')

def completeTest(request,**kwargs):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    test=Test.objects.get(id=kwargs['testID'])
    classobj=Class.objects.get(id=test.class_id_id)
    if not (Participant.objects.filter(course_id=classobj.course_id,user_id=request.user).exists() or Instructor.objects.filter(course_id=classobj.course_id,user_id=request.user).exists()):
        if not request.user.is_staff:
            return render(request, 'permission_error.html')
    try:
        Test.objects.get(id=kwargs['testID'])
    except Test.DoesNotExist:
        return render(request, 'test_error.html')
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
    if not (Participant.objects.filter(course_id=classobj.course_id,user_id=request.user).exists() or Instructor.objects.filter(course_id=classobj.course_id,user_id=request.user).exists()):
        if not request.user.is_staff:
            return render(request, 'permission_error.html')
    try:
        Test.objects.get(id=kwargs['testID'])
    except Test.DoesNotExist:
        return render(request, 'test_error.html')
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
    test=Test.objects.get(id=kwargs['testID'])
    classobj=Class.objects.get(id=test.class_id_id)    
    try:
        Instructor.objects.get(user_id_id=request.user.id,course_id_id=classobj.course_id_id)
    except Instructor.DoesNotExist:
        if not request.user.is_staff:
            return render(request, 'permission_error.html')
    try:
        Test.objects.get(id=kwargs['testID'])
    except Test.DoesNotExist:
        return render(request, 'test_error.html')
    c={
        'test':test,
        'users':CustomUser.objects.all(),
        'results':TestResult.objects.filter(test=test)
        }
    return render(request,"testScores.html",c)

def createTest(request,**kwargs):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    classobj=Class.objects.get(id=kwargs['classID'])    
    try:
        Instructor.objects.get(user_id_id=request.user.id,course_id_id=classobj.course_id_id)
    except Instructor.DoesNotExist:
        if not request.user.is_staff:
            return render(request, 'permission_error.html')
    f = CreateTestForm()

    c = {
        'form': f
    }
    if request.method == 'POST':
        testName = request.POST['name']
        testDesc = request.POST['description']
        ClassId = int(kwargs['classID'])
        t=Test(name=testName,description=testDesc,class_id_id=ClassId)
        t.save()
        return redirect('../../managetest/%d/addquestions' % t.id)
    return render(request,"createTest.html",c)


def addQuestions(request,**kwargs):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    test=Test.objects.get(id=kwargs['testID'])
    classobj=Class.objects.get(id=test.class_id_id)    
    try:
        Instructor.objects.get(user_id_id=request.user.id,course_id_id=classobj.course_id_id)
    except Instructor.DoesNotExist:
        if not request.user.is_staff:
            return render(request, 'permission_error.html')
    if request.method == 'POST':
            qText = request.POST['question_text']
            ans = [
                request.POST['answer_1'],
                request.POST['answer_2'],
                request.POST['answer_3'],
                request.POST['answer_4']
            ]
            corAns = request.POST['correct']
            testID = kwargs['testID']
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

    f=AddQuestionForm(request.POST)
    c = {
        'testID':kwargs['testID'],
        'form': f
    }
    return render(request,"addQuestions.html",c)

def editQuestion(request,**kwargs):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    test=Test.objects.get(id=kwargs['testID'])
    classobj=Class.objects.get(id=test.class_id_id)    
    try:
        Instructor.objects.get(user_id_id=request.user.id,course_id_id=classobj.course_id_id)
    except Instructor.DoesNotExist:
        if not request.user.is_staff:
            return render(request, 'permission_error.html')
    try:
        q=Question.objects.get(id=kwargs['questionID'])
    except Question.DoesNotExist:
        return render(request, 'editquestion_error.html')
    if request.method == 'POST':
            corAns = request.POST['correct']
            q=Question.objects.get(id=kwargs['questionID'])
            q.question_text = request.POST['question_text']
            ans=Answer.objects.filter(question_id=q)           
            q.save()
            i = 1
            for a in ans:
                a.answer_text = request.POST['answer_%d' % i]
                if i == int(corAns):
                    a.is_good=1
                else:
                    a.is_good=0
                a.save()
                i = i+1
            return redirect('editquestion',testID=kwargs['testID'],questionID=kwargs['questionID'])
    a=Answer.objects.filter(question_id=q)
    cor = 1
    for c in a:
        if c.is_good==1:
            break
        cor = cor+1
    f=AddQuestionForm(initial = {
        'answer_1':a[0].answer_text,
        'answer_2':a[1].answer_text,
        'answer_3':a[2].answer_text,
        'answer_4':a[3].answer_text,
        'correct':cor
    },
    instance=q)
    c = {
        'testID':kwargs['testID'],
        'form': f
    }
    return render(request,"editQuestion.html",c)

def manageTest(request,**kwargs):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    try:
        test=Test.objects.get(id=kwargs['testID'])
    except Test.DoesNotExist:
        return render(request, 'test_error.html')
    classobj=Class.objects.get(id=test.class_id_id)    
    try:
        Instructor.objects.get(user_id_id=request.user.id,course_id_id=classobj.course_id_id)
    except Instructor.DoesNotExist:
        if not request.user.is_staff:
            return render(request, 'permission_error.html')
    c={
        'test':test,
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
        return redirect('courses', 1)
    return render(request,'addcourse.html',{'form': f})

def JoinCourse(request,kurs):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    if not request.user.has_perm('dbhandler.add_participant'):
        return render(request, 'permission_error.html')
    course=Course.objects.get(id=kurs)
    user=request.user
    if Participant.objects.filter(course_id=course,user_id=user).exists() or Instructor.objects.filter(course_id=course,user_id=user).exists():
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
        if len(Instructor.objects.filter(course_id=k))==1:
            messages.error(request, 'Jesteś jedynym prowadzącym tego kursu')
        else:
            Instructor.objects.get(course_id=k, user_id=u).delete()

    if Participant.objects.filter(course_id=k,user_id=u).exists():
        Participant.objects.get(course_id=k, user_id=u).delete()
        messages.success(request, 'Nie należysz juz do kursu')
    return redirect('user_courses', 1)

def EditCourse(request,kurs):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    course = Course.objects.filter(id=kurs).first()
    user=request.user
    if not Instructor.objects.filter(course_id=course, user_id=user).exists():
        messages.error(request,"Nie jesteś prowadzącym tego kursu")
        return redirect('course_detail', kurs)
    f = AddCourseForm(instance=course)
    if request.method == 'POST':
        course.name = request.POST['name']
        course.course_type = CourseType.objects.get(id=request.POST['course_type'])
        course.module_id = Module.objects.get(id=request.POST['module_id'])
        course.description = request.POST['description']
        course.password = request.POST['password']
        course.save()
        messages.success(request, 'Zaktualizowano dane kursu')
        return redirect('course_detail', kurs)
    return render(request, 'changeCourseData.html', {'form': f})

def UserCourses(request,**kwargs):
    if not request.user.is_authenticated:
        messages.error(request, 'Musisz być zalogowany aby zobaczyć swoje kursy')
        return redirect('index')
    id_course_list=[]
    for p in Participant.objects.filter(user_id=request.user):
        id_course_list.append(p.course_id.id)
    for i in Instructor.objects.filter(user_id=request.user):
        if not i.course_id.id in id_course_list:
            id_course_list.append(i.course_id.id)
    k=Instructor.objects.filter(course_id__id__in=id_course_list)
    fname=''
    lname=''
    cname=''
    mname=''
    if 'course_name' in request.GET:
        if request.GET['course_name'] is not '':
            cname=request.GET['course_name']
            k=k.filter(course_id__name__contains=cname)
    if 'instr_name' in request.GET:
        if request.GET['instr_name'] is not '':
            fname=request.GET['instr_name']
            k=k.filter(user_id__first_name__contains=fname)
    if 'instr_lastname' in request.GET:
        if request.GET['instr_lastname'] is not '':
            lname=request.GET['instr_lastname']
            k=k.filter(user_id__last_name__contains=lname)
    if 'module_name' in request.GET:
        if request.GET['module_name'] is not '':
            mname=request.GET['module_name']
            k=k.filter(course_id__module_id__name__contains=mname)
    search_query = '?course_name='+cname+'&instr_name='+fname+'&instr_lastname'+lname+'&module_name='+mname

    page = kwargs['page']

    paginator = Paginator(k, 10)
    try:
        k = paginator.page(page)
    except PageNotAnInteger:
        k = paginator.page(1)
    except EmptyPage:
        k = paginator.page(paginator.num_pages)
    c = {
        'search_query':search_query,
        'courses':k,
    }
    return render(request, 'user_courses.html', c)

def AddCourseInstructor(request,kurs):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    course= Course.objects.filter(id=kurs).first()
    user=request.user
    if not Instructor.objects.filter(course_id=course, user_id=user).exists():
        messages.error(request,"Nie jesteś prowadzącym tego kursu")
        return redirect('course_detail', kurs)
    f=AddInstructorForm(request.POST)
    if request.method=='POST':
        newInstructorUser_id=request.POST['user_id']
        if Instructor.objects.filter(course_id=course, user_id=newInstructorUser_id).exists():
            messages.error(request, 'Podany użytkownik jest już instruktorem tego kursu')
            return redirect('course_detail', kurs)
        newInstructorUser=CustomUser.objects.get(pk=newInstructorUser_id)
        newInstructor=Instructor()
        newInstructor.course_id=course
        newInstructor.user_id=newInstructorUser
        newInstructor.save()
        messages.success(request, 'Dodano nowego prowadzącego')
        return redirect('course_detail', kurs)
    return render(request,'addCourseInstructor.html',{'form': f})

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
        contentData = Content()
        contentData.text = request.POST.get('content')
        contentData.class_id = classData
        contentData.save()
        return redirect('class', classData.id)
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

def EditClass(request,classId):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    if not request.user.has_perm('dbhandler.change_class'):
        return render(request, 'class_error.html')
    
    if request.method == 'POST':
        k = Class.objects.get(pk=classId)
        if not k:
            #Change to django messages system
            return HttpResponse("Wystąpił błąd!")

        k.name=request.POST.get('name')
        k.description = request.POST.get('description')
        k.course_id = Course.objects.get(id=request.POST['course_id'])
        k.save()
        cont = Content.objects.get(class_id=k, valid_until__isnull=True)
        cont.valid_until=datetime.now()
        cont.save()
        new_cont = Content()
        new_cont.class_id = k
        new_cont.text=request.POST.get('content')
        new_cont.save()
        return redirect('class', k.id)

    k = Class.objects.get(pk=classId)
    cont = Content.objects.get(class_id=k, valid_until__isnull=True)
    if not k:
        #Change to django messages system
        return HttpResponse("Wystąpił błąd!") 

    f=AddClassForm(initial = {
        'content':cont.text
    },
    instance=k)

    c = {
        'form': f
    }

    return render(request, "class_edit.html", c)

