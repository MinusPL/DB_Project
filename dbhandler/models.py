from django.db import models
from django.contrib.auth.models import AbstractUser

# Modele

class Module(models.Model):
    name = models.CharField(max_length=64)

class CourseType(models.Model):
    name = models.CharField(max_length=64)

class InstructorData(models.Model):
    home_page = models.CharField(max_length = 40)

class CustomUser(AbstractUser):
    pass
    instructor_data = models.ForeignKey('InstructorData', on_delete=models.CASCADE, null=True, blank=True)

class Course(models.Model):
    name = models.CharField(max_length = 64)
    course_type = models.ForeignKey('CourseType', on_delete=models.CASCADE)
    module_id = models.ForeignKey('Module', on_delete=models.CASCADE)
    description = models.TextField()
    password = models.CharField(max_length = 16)
    def __str__(self):
        return self.name
        
class Instructor(models.Model):
    user_id = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE)

class Participant(models.Model):
    user_id = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE)

class Class(models.Model):
    name = models.CharField(max_length = 64)
    description = models.TextField()

class Content(models.Model):
    valid_until = models.DateTimeField()
    text = models.TextField()
    class_id = models.ForeignKey('Class', on_delete=models.CASCADE)

class Comment(models.Model):
    text = models.TextField()
    author_id = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    class_id = models.ForeignKey('Class', on_delete=models.CASCADE)

class Test(models.Model):
    name = models.CharField(max_length = 64)
    description = models.TextField()
    class_id = models.ForeignKey('Class', on_delete=models.CASCADE)

class Question(models.Model):
    question_text = models.TextField()
    test_id = models.ForeignKey('Test', on_delete=models.CASCADE)

class Answer(models.Model):
    answer_text = models.TextField()
    is_good = models.SmallIntegerField()
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE)

