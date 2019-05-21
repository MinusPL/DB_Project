from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username']

admin.site.register(Module)
admin.site.register(CourseType)
admin.site.register(InstructorData)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Course)
admin.site.register(Instructor)
admin.site.register(Participant)
admin.site.register(Class)
admin.site.register(Content)
admin.site.register(Comment)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(TestResult)





