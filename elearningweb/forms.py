from django import forms
from django.forms import ModelForm
from ckeditor.widgets import CKEditorWidget
from dbhandler.models import Course, Test, Answer, Question, Class, Instructor


class CreateTestForm(ModelForm):
    class Meta:
        model=Test
        fields = ('name','description')
        labels = {
            'name': ('Nazwa'),
            'description': ('Opis'),
        }

class AddQuestionForm(ModelForm):
    answer_1 = forms.CharField(label="Odpowiedź 1")
    answer_2 = forms.CharField(label="Odpowiedź 2")
    answer_3 = forms.CharField(label="Odpowiedź 3")
    answer_4 = forms.CharField(label="Odpowiedź 4")
    correct = forms.ChoiceField(choices=[('1','Odpowiedź 1'),('2','Odpowiedź 2'),('3','Odpowiedź 3'),('4','Odpowiedź 4')], widget=forms.RadioSelect(), label="Prawidłowa odpowiedź", required=False)
    class Meta:
        model=Question
        fields = ('question_text',)
        labels = {
            'question_text': ('Treść pytania')
        }
        widgets = {
            'question_text': CKEditorWidget()
        }

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