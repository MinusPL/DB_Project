from django.shortcuts import render, redirect
from urllib.parse import urlencode
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from dbhandler.models import Course, CourseType, Module, Instructor, Participant, CustomUser
from dbhandler.forms import AddCourseForm

# Create your views here.

class CoursesView(ListView):
    model = Course
    template_name = 'courses.html'

#class UserCoursesView(ListView):
#    model = Course
#    template_name = 'user_courses.html'
#    for course in Course.objects.all():
#        if Participant.filter(course=course, user=self.reques.user)
#    def get_context_data(self, **kwargs):
#        context = super(UserCoursesView, self).get_context_data(**kwargs)
#        context['courses']=Course.objects.all()
#        Participants
#        return context

class CourseDetailView(DetailView):
    model = Course
    template_name='course_detail.html'
    #CustomUser=get_user()
    #if Participant.objects.filter(course_id=Course,user_id=).exists():
    #    template_name = 'course_detail.html'
    #else:
    #    redirect("{% url 'course_detail' course.id %}")

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
        course=Course()
        course.name=request.POST['name']
        if Course.objects.filter(name=course.name).exists():
            #TUTAJ JAKIS KOMUNIKAT ZE ZAJETE
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
    k=Course.objects.filter(id=kurs).first()
    u=request.user
    if Participant.objects.filter(course_id=k,user_id=u).exists():
        return redirect('course_detail', k.pk)
    else:
        if request.method=='POST':
            pa=request.POST['coursepass']
            if pa==k.password:
                p=Participant()
                p.course_id=k
                p.user_id=u
                p.save()
                return redirect('course_detail',k.pk)
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

def UserCourses(request):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    i=0
    k=Course.objects.none()
    id_course_list=[]
    for p in Participant.objects.filter(user_id=request.user):
        id_course_list.append(p.course_id.id)
    k=Course.objects.filter(id__in=id_course_list)
    return render(request, 'user_courses.html', {'courses': k})
