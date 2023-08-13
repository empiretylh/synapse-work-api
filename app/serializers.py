from rest_framework import serializers
from django.contrib.auth import get_user_model
from . import models

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError

from django.utils import timezone


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'})

    class Meta:
        model = get_user_model()
        fields = ['name', 'username', 'password','is_admin','email']
        write_only_fields = ('password')

    def create(self, validated_data):
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.start_d = timezone.now()
        user.end_d = timezone.now()
        user.save()

        return user


User = get_user_model()


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id','name','username','email','password','is_admin','profileimage']

class LessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lessons
        fields = ['id','course','title','content']    



class CourseSerializer(serializers.ModelSerializer):
  
    
    class Meta:
        model = models.Course
        fields = ['id','coverimage','course_name','short_name','course_price','description','avaliable']
