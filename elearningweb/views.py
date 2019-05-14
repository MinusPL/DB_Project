from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dbhandler.models import Course, Test

# Create your views here.

class CoursesView(ListView):
    model = Course
    template_name = 'courses.html'
    #login_url = "/elearning/login/"
    #redirect_field_name = "redirect_to"

class HomeView(TemplateView):
    template_name = 'index.html'

class TestView(ListView):
    model = Test
    template_name = 'test.html'
    #login_url = "/elearning/login/"
    #redirect_field_name = "redirect_to"