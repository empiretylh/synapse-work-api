from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser, Group

from django.core.files.base import ContentFile
from polymorphic.models import PolymorphicModel

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=255, null=False)
    profileimage = models.ImageField(
        upload_to="img/profile/%y/%mm/%dd", null=True)
    email = models.EmailField(unique=True,null=True)

    phone = models.CharField(max_length=255, null=True)


    is_admin = models.BooleanField(default=False)
    is_editor = models.BooleanField(default=False)

    course = models.ManyToManyField('Course',through='CourseMember',related_name='people')
    coursereq = models.ManyToManyField('Course',through='CourseRequest',related_name='peoplereq')

# I want to store user's login devices in database
# so I create a new table to store user's login devices
class UserDevice(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_device')
    device = models.CharField(max_length=255)
    fcm_token =  models.CharField(max_length=255,null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True) # when user login
    updated_at = models.DateTimeField(auto_now=True) # when user logout

    def __str__(self):
        return self.user.username + ": : " + self.device


class Course(models.Model):
    coverimage = models.ImageField(upload_to="img/%y",null=True)
    course_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100,null=True)
    course_price = models.CharField(max_length=50)
    description = models.TextField(blank=True,null=True)
    avaliable = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='created_user')
    payment_info = models.TextField(blank=True,null=True, default="KBZ Pay - 09699227094 (Mg Thura Lin Htut)")
    telegram = models.CharField(max_length=100, default="synapsework")
    semester = models.CharField(max_length=100, default="Semester 2")


    def __str__(self):
        return self.course_name

# in courses there are many course_menu_groups that contains many course_menus and content

class CourseMenuGroup(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='category')
    title = models.CharField(max_length=50)
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
       return self.title

class Content(PolymorphicModel):
    order = models.IntegerField()
    course_menu = models.ForeignKey(CourseMenuGroup,on_delete=models.CASCADE,related_name='content')
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
     
    def __str__(self):
       return self.title



class CourseMember(models.Model):
    person = models.ForeignKey(User,related_name='membership',on_delete=models.CASCADE)
    course = models.ForeignKey(Course,related_name='membership',on_delete=models.CASCADE)

    def __str__(self):
        return "%s is in group %s" % (self.person,self.course)

class CourseRequest(models.Model):
    coursename = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    confirm = models.BooleanField(default=False)
    joindate = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Lessons(Content):
    #lesson_title = models.CharField(max_length=50)
    content = models.TextField()

    def __str__(self):
       return self.title

# Question and answer model
class QnA(Content):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    def __str__(self):
        return self.title


class Quiz(Content):
    question = models.CharField(max_length=255)
    answers = models.ManyToManyField('Answer')
    correct_answer = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='correct_answer')

    def __str__(self):
        return self.title

class Answer(models.Model):
    answer_text = models.CharField(max_length=255)


# from django.db import models

class Notification(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    action_url = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sended_device = models.ManyToManyField(UserDevice)