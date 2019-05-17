from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm, CustomUserChangeForm, GroupAdminForm

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

admin.site.unregister(Group)

# Create a new Group admin.
class GroupAdmin(admin.ModelAdmin):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']

# Register the new Group ModelAdmin.
admin.site.register(Group, GroupAdmin)




