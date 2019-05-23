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
