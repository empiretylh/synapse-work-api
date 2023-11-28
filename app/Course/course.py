from rest_framework.permissions import AllowAny
from ..serializers import CourseRequestSerializer
from ..models import CourseRequest
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from ..models import Course, CourseMenuGroup, UserDevice, Notification
from ..serializers import CourseSerializer, CourseReadSerializer, CourseMenuGroupSerializer, CreateCourseMenuGroupSerializer, EditCourseMenuGroupSerializer, CourseRequestUpdateSerializer
from ..Noti.firebasenoti import send_multicast_message

class CourseAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_admin or user.is_editor:
            serializer.save()
        return super().perform_create(serializer)


class CourseListAPIView(generics.ListAPIView):
    serializer_class = CourseReadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        course_id = self.request.query_params.get('course_id')
        print(course_id)
        if user.is_admin:
            queryset = Course.objects.all()
        elif user.is_editor:
            queryset = Course.objects.filter(created_by=user)
        else:
            queryset = Course.objects.filter(avaliable=True)
        if course_id:
            queryset = queryset.filter(id=course_id)
        return queryset


class IsCourseCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user or request.user.is_admin


class CourseEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsCourseCreator]


class CourseDeleteAPIView(generics.DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsCourseCreator]


# Course Menu Group API VIEW--------------------------------------------------------------------

class CourseMenuGroupListCreateAPIView(generics.ListCreateAPIView):
    queryset = CourseMenuGroup.objects.all()
    serializer_class = CreateCourseMenuGroupSerializer


class CourseMenuGroupRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CourseMenuGroup.objects.all()
    serializer_class = EditCourseMenuGroupSerializer


class CourseMenuGroupListAPIView(generics.ListAPIView):
    serializer_class = CourseMenuGroupSerializer
    permission_classes = [AllowAny]

    # Course Menu Group filter by course id
    def get_queryset(self):
        course_id = self.request.query_params.get('course_id')
        if course_id:
            queryset = CourseMenuGroup.objects.filter(course__id=course_id)
        else:
            queryset = CourseMenuGroup.objects.all()
        return queryset


class CourseMenuGroupDeleteAPIView(generics.DestroyAPIView):
    queryset = CourseMenuGroup.objects.all()
    serializer_class = CourseMenuGroupSerializer
    permission_classes = [permissions.IsAuthenticated, IsCourseCreator]


# CourseRequest


class CourseRequestListCreateAPIView(generics.ListCreateAPIView):
    queryset = CourseRequest.objects.all()
    serializer_class = CourseRequestSerializer
    permission_classes = [permissions.IsAuthenticated]


# Get list

class CourseRequestListAPIView(generics.ListAPIView):
    serializer_class = CourseRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            queryset = CourseRequest.objects.all()
        elif user.is_editor:
            queryset = CourseRequest.objects.filter(
                coursename__created_by=user)
        else:
            queryset = CourseRequest.objects.filter(user=user)

        print(user, queryset)
        return queryset

# Update and Destory


class CourseRequestRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CourseRequest.objects.all()
    serializer_class = CourseRequestUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Permission only course creator and admin
    def perform_update(self, serializer):
        user = self.request.user
        if user.is_admin or user.is_editor:
            instance =  serializer.save()
          
          
            user_device = UserDevice.objects.filter(user=instance.user)

            fcm_tokens = []
            for ud in user_device:
                fcm_tokens.append(ud.fcm_token)

            coursename = instance.coursename.course_name

            title = "Course Request Approved!"
            message = "You request for " + coursename + " is approved! You can now access to this course."
            data = {
                "url": "sw://course/" + str(instance.coursename.id)
            }

            notification = Notification.objects.create(
                title=title, message=message, action_url=data['url'])
            
            notification.sended_device.set(user_device)

            send_multicast_message(fcm_tokens, title, message, data)
           

            
            

         

        return super().perform_update(serializer)
