from django.shortcuts import render

# Create your views here.

def index(request):
    
    context = {

    }

    return render(request, 'index.html', context=context)

from dbhandler.models import Course, CourseType, Module

def courses(request):
    
    num_courses = Course.objects.all().count()
    num_modules = Module.objects.all().count()

    context = {
        'num_courses': num_courses,
        'num_modules': num_modules,
    }

    return render(request, 'courses.html', context=context)