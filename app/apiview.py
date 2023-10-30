import operator
import functools
import collections
from collections import OrderedDict
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.decorators import user_passes_test

# A Python program to demonstrate working of OrderedDict
from collections import OrderedDict

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView

from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone


from django.db.models import Q




from . import models, serializers

import json
    



def CHECK_IN_PLAN_AND_RESPONSE(user, data, **args):
    if user.is_plan:
        return Response('End Plan or No Purchase Plan')
    else:
        return Response(data=data, **args)

    print('User is in Plan')


class UserChangePasswordView(APIView):

    def put(self, request):
        newpassword = request.data['new_password']
        print(request.data)
        if 'old_password' in request.data:
            user = authenticate(request, username=request.user.username, password=request.data['old_password'])
        else:
            user = models.User.objects.get(username=request.user)
        if user is not None:
            user.set_password(newpassword)
            user.save()
            return Response({'message':'Password Change Success'},status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Invalid old password'}, status=status.HTTP_401_UNAUTHORIZED)


class ForgotPasswordView(APIView):
    serializer_class = serializers.ForgotPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = models.User.objects.get(email=serializer.validated_data['email'])
        token, created = Token.objects.get_or_create(user=user)
        
        email = request.data['email']

#         subject = 'TMT Agency Account Reset Password'


#         CI = models.CompanyInformation.objects.last()

#         html_content = '''<html>
# <head>
   
# <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">


# <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

# <script src="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
# <style>
#  .reset-password-btn {
#  text-decoration:none;
#   background-color: blue;
#   color: #fff;
#   border: none;
#   border-radius: 4px;
#   padding: 10px 20px;
#   font-size: 16px;
#   cursor: pointer;
# }

# .reset-password-btn:hover {
#   background-color: darkblue;
# }
# In this code, the background-color property sets the background color of the button to blue, while the color property sets the text color to white. The border, border-radius, and padding properties are used to style the button, while the `font-size




# </style>
# </head>
# <body>
#   <div>
#       <p> <strong>Dear '''+user.name+'''</strong>, <br/><br/>
#         We have received a request to rest the password associated with your account. To proceed with resetting your password, please click on the "Rest Password" button bellow. This will take you to a secure page where you can enter a new password for your account.
#          <br/>
#            <br/>
#         Company : '''+CI.companyname+'''<br/>
#         Call Center : <a href="tel:'''+CI.phoneno+'''">'''+CI.phoneno+'''</a><br/>
#         Email : '''+CI.email+'''<br/>
#         Company Address : '''+CI.companyaddress+'''<br/>
#     </p>  
#     </div>
# <div class='container'>
# <a class='reset-password-btn' href="https://tmtagency.github.io/travel/#/restpassword/'''+str(token)+'''">
# Reset Password
# </a>
# <p>
# If you are unable to clck on the button below, please copy and paste the following URL into your web browser:<br/>
#  https://tmtagency.github.io/travel/#/restpassword/'''+str(token)+'''<br/>
# </p>
# </div>
# </body>
# </html>
#         '''        


#         SENDEMAIL = EmailMessage(subject, html_content, 'traveleragencymm@gmail.com', [
#                                  email], headers={'Message-ID': user.id})
#         SENDEMAIL.content_subtype = "html"
#         SENDEMAIL.send()
#         # TODO: Send the password reset link to the user's email address
#         # email = ...
#         # send_email(email, uid, token)

        return Response({'detail': 'Password reset link has been sent to your email address.'}, status=status.HTTP_200_OK)


class LoginView(APIView):

    permission_classes = [AllowAny]


    def post(self, request, *args, **kwargs):
      
        print(request.data)

        username_or_email = request.data['username']
        password = request.data['password']

        # user devices
        device = request.data.get('device', None)

        user = None
        if '@' in username_or_email:
            b = models.User.objects.get(email=username_or_email)
            user = authenticate(username=b.username, password=password)
        else:
            user = authenticate(username=username_or_email, password=password)

        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_401_UNAUTHORIZED)

        # user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        # user device
        models.UserDevice.objects.create(user=user,device=device)


        # add custom data to response
        response_data = {
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin,
            # add additional data fields here as needed
        }


        return Response(response_data)

class CreateUserApiView(CreateAPIView):

    permission_classes = [AllowAny]
    serializer_class = serializers.CreateUserSerializer

    def post(self, request):

        print(request.data)
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        self.perform_create(serializers)
        headers = self.get_success_headers(serializers.data)

        # Create a token than will be used for future auth
        token = Token.objects.create(user=serializers.instance)
        token_data = {'token': token.key}

        return Response(
            {**serializers.data, **token_data},
            status=status.HTTP_201_CREATED,
            headers=headers)


class UserApiView(APIView):

    permission_classes = [AllowAny]

    def get(self,request):
        types = request.GET.get('type')
        print(request.GET)
        user = models.User.objects.get(username=request.user)
        if types == 'all':
            users = models.User.objects.all()
            ser = serializers.UserSerializer(users,many=True)
        else:
            users = user
            ser = serializers.UserSerializer(users)
        

        return Response(ser.data)

    def put(self,request):
      id = request.GET.get('id')

      user = models.User.objects.get(id=id)
      user.name = request.data.get('name',user.name) 
      user.email = request.data.get('email', user.email) 
      user.phone = request.data.get("phone",user.phone) 
      user.username = request.data.get("username",user.username) 
      user.is_admin = request.data.get("admin",user.is_admin)
      user.is_editor = request.data.get("editor",user.is_editor)

      user.save()

      return Response(1)

    def delete(self,request):
        current_user = models.User.objects.get(username=request.user)
        userid = request.GET.get('id')
        if current_user.is_admin :
       
            user = models.User.objects.get(id=userid)
            user.delete()

        return Response(1)              



class CourseAPIView(APIView):
    def get(self,request,format=None):
        
        if request.user:
            coursesuserget = models.Course.objects.filter(people=request.user)
            allcourse = models.Course.objects.filter(~Q(peoplereq=request.user))
            reqcourse = models.CourseRequest.objects.filter(user=request.user,confirm=False)


            c = []
            for a in reqcourse:
                c.append(a.coursename)
            
            coursesusergetserializer = serializers.CourseSerializer(coursesuserget,many=True)
            allcourseserializer = serializers.CourseSerializer(allcourse,many=True)

            reqcourseserializer = serializers.CourseSerializer(c,many=True)

            twoserializer = {
                'courseuserget' : coursesusergetserializer.data,
                'allcourse': allcourseserializer.data,
                'coursereq': reqcourseserializer.data,
            
            }
            
            return Response(twoserializer)
        
        twoserializer = {
                'courseuserget' : {},
                'allcourse':{},
                'coursereq': {},
            
            }
            
        return Response(twoserializer)



    def post(self,request,format=None):
      print(request.data['courseid'])
      course_id = request.data['courseid']
      course = models.Course.objects.get(id=course_id)
      models.CourseRequest.objects.create(coursename=course,user=request.user)

      return Response(status=status.HTTP_201_CREATED)


class LessonAPIView(APIView):
    # type = one or all or onlytitle
    # courseid
    # lessonid

    def get(self,request,format=None):
        course_id = request.GET.get('courseid')
        course_type = request.GET.get('type')
        lesson_id = request.GET.get('lessonid')

        course = models.Course.objects.get(id=course_id)    
       
        if course_type == 'all':
            lesson = models.Lessons.objects.filter(course=course)
            se = serializers.LessonsSerializer(lesson,many=True)
        elif course_type == 'one':
            lesson = models.Lessons.objects.get(course=course,id=lesson_id)
            se = serializers.LessonsSerializer(lesson)
        elif course_type == 'onlytitle':
            lesson = models.Lessons.objects.filter(course=course)
            c = []
            for a in lesson:
                c.append({"id": a.id , "title" : a.title})
                
            return Response(c)
        
        return Response(se.data)

    # only admin user can post lesson
    @user_passes_test(lambda u: u.is_admin)
    def post(self,request,format=None):
        course_id = request.data['courseid']
        title = request.data['title']
        content = request.data['content']
        models.Lessons.objects.create(course_id=course_id,title=title,content=content)
        
        return Response(status=status.HTTP_201_CREATED)
    
    # only admin user can put lesson
    @user_passes_test(lambda u: u.is_admin)
    def put(self,request,format=None):
        lesson_id = request.data['lessonid']
        title = request.data['title']
        content = request.data['content']
        lesson = models.Lessons.objects.get(id=lesson_id)
        lesson.title = title
        lesson.content = content
        lesson.save()
        return Response(status=status.HTTP_201_CREATED)
    
    # only admin user can delete lesson
    @user_passes_test(lambda u: u.is_admin)
    def delete(self,request,format=None):
        lesson_id = request.GET.get('lessonid')
        lesson = models.Lessons.objects.get(id=lesson_id)
        lesson.delete()
        return Response(status=status.HTTP_201_CREATED) 
    