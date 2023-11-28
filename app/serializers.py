from rest_framework import serializers
from django.contrib.auth import get_user_model
from . import models

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from .models import User, Course, Content, CourseMember, CourseMenuGroup, CourseRequest, Lessons, QnA, Quiz, Answer
from .Noti.firebasenoti import send_multicast_message

from django.utils import timezone


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'})

    class Meta:
        model = get_user_model()
        fields = ['name', 'username', 'password','email', 'phone']
        write_only_fields = ('password')

    def create(self, validated_data):
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            raise ValidationError('Invalid email address')
        return user.email
    
    class Meta:
        model = User
        fields = ['email']


        model = CourseRequest
        fields = ['id', 'coursename', 'user', 'confirm', 'joindate', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'profileimage', 'email', 'phone', 'is_admin', 'is_editor', 'course', 'coursereq']

class CourseSerializer(serializers.ModelSerializer):
    # created_user = UserSerializer()
    class Meta:
        model = Course
        fields = ['id', 'coverimage', 'course_name', 'short_name', 'course_price', 'description','avaliable', 'created_at', 'updated_at','payment_info','telegram','semester']

    def create(self, validated_data):
        user = self.context['request'].user 
        validated_data['created_by'] = user
        return super().create(validated_data)
    
class CourseMenu_Course(serializers.ModelSerializer):
    class Meta:
        model = CourseMenuGroup
        fields = ['id', 'title', 'order']  # Add other fields as needed


class CourseReadSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    category = CourseMenu_Course(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'coverimage', 'course_name', 'short_name', 'course_price', 'description', 'avaliable', 'created_at', 'updated_at', 'created_by','category','payment_info','telegram','semester']

    def get_created_by(self, obj):
        return obj.created_by.username 

class CreateCourseMenuGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMenuGroup
        fields = ['course', 'title']

    # create order value automatically
    def create(self, validated_data):
        course = validated_data['course']
        order = CourseMenuGroup.objects.filter(course=course).count() + 1
        validated_data['order'] = order
        return super().create(validated_data)
    

class EditCourseMenuGroupSerializer(serializers.ModelSerializer): #it contains order
    class Meta:
        model = CourseMenuGroup
        fields = ['id', 'course', 'title','order', 'created_at', 'updated_at']
    

class CourseMenuGroupSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
   
    class Meta:
        model = CourseMenuGroup
        fields = ['id', 'course', 'title', 'order', 'created_at', 'updated_at']



class ContentSerializer(serializers.ModelSerializer):
    course_menu = CourseMenuGroupSerializer()
    class Meta:
        model = Content
        fields = ['id', 'order', 'course_menu', 'title', 'created_at', 'updated_at']

class CourseMemberSerializer(serializers.ModelSerializer):
    person = UserSerializer()
    course = CourseSerializer()
    class Meta:
        model = CourseMember
        fields = ['id', 'person', 'course']

class CourseRequestSerializer(serializers.ModelSerializer):
    coursename = CourseReadSerializer()
    user = UserSerializer()
    class Meta:
        model = CourseRequest
        fields = ['id', 'coursename', 'user', 'confirm', 'joindate', 'created_at', 'updated_at']

class CourseRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRequest
        fields = ['id', 'confirm', 'created_at', 'updated_at']


class LessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = ['id', 'order', 'course_menu', 'title', 'created_at', 'updated_at', 'content']


class QnASerializer(serializers.ModelSerializer):
    class Meta:
        model = QnA
        fields = ['id', 'order', 'course_menu', 'title', 'created_at', 'updated_at', 'question', 'answer']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer_text']

class QuizSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    correct_answer = AnswerSerializer()
    class Meta:
        model = Quiz
        fields = ['id', 'order', 'course_menu', 'title', 'created_at', 'updated_at', 'question', 'answers', 'correct_answer']

#  user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_device')
#     device = models.CharField(max_length=255)
#     fcm_token =  models.CharField(max_length=255,null=True, default=None)
#     created_at = models.DateTimeField(auto_now_add=True) # when user login
#     updated_at = models.DateTimeField(auto_now=True) # when user logout

class UserDeviceSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = models.UserDevice
        fields = ['id', 'user', 'device', 'fcm_token', 'created_at', 'updated_at']


#    title = models.CharField(max_length=255, null=True, blank=True)
#     message = models.TextField(null=True, blank=True)
#     action_url = models.URLField(max_length=500, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     sended_device = models.ManyToManyField(UserDevice)
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = ['id', 'title', 'message', 'action_url', 'created_at', 'updated_at', 'sended_device']
    