from django import forms
from django.forms import ModelForm
from ckeditor.widgets import CKEditorWidget
from dbhandler.models import Course, Test, Answer, Question, Class, Instructor


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
            'module_id' : ('Przedmiot'),
            'description': ('Opis Kursu'),
            'password' : ('Hasło do Kursu')
        }
class AddInstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ('user_id',)
        labels = {
            'user_id': ('Prowadzący')
        }


class AddClassForm(ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model=Class
        fields = ('name','description','course_id')
        labels = {
            'name': ('Nazwa Zajęć'),
            'description' : ('Opis'),
            'course_id' : ('Kurs')
        }