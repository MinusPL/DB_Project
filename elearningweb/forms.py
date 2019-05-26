from django import forms
from django.forms import ModelForm
from dbhandler.models import Course, Test, Answer, Question, Class

class QuestionForm():
        class Meta:
            model = Question
            fields = ['question_text']

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text','is_good']

class AddCourseForm(forms.ModelForm):
    class Meta:
        model=Course
        fields = ('name','course_type','module_id','description','password')
        labels = {
            'name': ('Nazwa Kursu'),
            'course_type' : ('Typ Kursu'),
            'module_id' : ('Moduł Kursu'),
            'description': ('Opis Kursu'),
            'password' : ('Hasło do Kursu')
        }

class AddClassForm(ModelForm):
    class Meta:
        model=Class
        fields = ('name','description','course_id')
        labels = {
            'name': ('Nazwa Zajęć'),
            'description' : ('Opis'),
            'course_id' : ('Kurs')
        }