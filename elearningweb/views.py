from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dbhandler.models import Course, CourseType, Module, Instructor
from dbhandler.forms import AddCourseForm

# Create your views here.

class CoursesView(ListView):
    model = Course
    template_name = 'courses.html'
    #login_url = "/elearning/login/"
    #redirect_field_name = "redirect_to"

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
    return render(request,'addcourse.html',{'form': f})