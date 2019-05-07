from django.db import models

# Modele

class Module(models.Model):
    name = models.CharField(max_length=64)

class CourseType(models.Model):
    name = models.CharField(max_length=64)

class InstructorData(models.Model):
    home_page = models.CharField(max_length = 40)

class User(models.Model):
    account_type = models.IntegerField()
    imie = models.CharField(max_length=16)
    nazwisko = models.CharField(max_length=32)
    mail = models.CharField(max_length=32)
    instructor_data = models.ForeignKey('InstructorData', on_delete=models.CASCADE, null=True, blank=True)

class Course(models.Model):
    name = models.CharField(max_length = 64)
    course_type = models.ForeignKey('CourseType', on_delete=models.DO_NOTHING)
    module_id = models.ForeignKey('Module', on_delete=models.DO_NOTHING)
    description = models.TextField()
    password = models.CharField(max_length = 16)

class Instructor(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE)

class Participant(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE)

class Class(models.Model):
    name = models.CharField(max_length = 64)
    description = models.TextField()

class Content(models.Model):
    valid_until = models.DateTimeField()
    text = models.TextField()
    class_id = models.ForeignKey('Class', on_delete=models.DO_NOTHING)

class Comment(models.Model):
    text = models.TextField()
    author_id = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    class_id = models.ForeignKey('Class', on_delete=models.DO_NOTHING)

class Test(models.Model):
    description = models.TextField()
    class_id = models.ForeignKey('Class', on_delete=models.CASCADE)

class Question(models.Model):
    question_text = models.TextField()
    test_id = models.ForeignKey('Test', on_delete=models.CASCADE)

class Answer(models.Model):
    answer_text = models.TextField()
    is_good = models.SmallIntegerField()
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE)

