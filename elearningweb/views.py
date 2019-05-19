from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from dbhandler.models import Course, CourseType, Module, Instructor, Participant
from dbhandler.forms import AddCourseForm, CourseListForm

# Create your views here.

class CoursesView(ListView):
    model = Course
    template_name = 'courses.html'

class CourseDetailView(DetailView):
    model = Course
    template_name = 'course_detail.html'

class HomeView(TemplateView):
    template_name = 'index.html'

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
        k=Course()
        k.name=request.POST['name']
        k.course_type = CourseType.objects.get(id=request.POST['course_type'])
        k.module_id = Module.objects.get(id=request.POST['module_id'])
        k.description= request.POST['description']
        k.password=request.POST['password']
        if Course.objects.filter(name=k.name).exists():
            return redirect('addcourse')
        k.save()

        instr = Instructor()
        instr.course_id = k
        instr.user_id = request.user
        instr.save()
        return redirect('courses')
    return render(request,'addcourse.html',{'form': f})

def JoinCourse(request,kurs):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    if not request.user.has_perm('dbhandler.add_participant'):
        return render(request, 'permission_error.html')
    k=Course.objects.filter(id=kurs).first()
    u=request.user
    if not Participant.objects.filter(course_id=k,user_id=u).exists():
        if request.method=='POST':
            pa=request.POST['coursepass']
            if pa==k.password:
                p=Participant()
                p.course_id=k
                p.user_id=u
                p.save()
                return redirect('courses')
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
        #return HttpResponse("Nie bierzesz juz udzialu w tym kursie")
    return redirect('courses')