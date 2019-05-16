from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dbhandler.models import Course, Test, Answer, Question

# Create your views here.

class CoursesView(ListView):
    model = Course
    template_name = 'courses.html'
    #login_url = "/elearning/login/"
    #redirect_field_name = "redirect_to"

class HomeView(TemplateView):
    template_name = 'index.html'

class TestsView(ListView):
    model = Test
    def get_context_data(self, **kwargs):
        context = super(TestsView, self).get_context_data(**kwargs)
        context['questions'] = Question.objects.all()
        context['answers'] = Answer.objects.all()
        return context
    template_name = 'tests.html'