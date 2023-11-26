from django.urls import path, include

# from app.models import SalesTwoDigits
from . import views
from . import apiview
from django.conf.urls.static import static
from django.conf import settings
from .Course import course
from .Lesson import lesson
from .Noti import Noti
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [

    path('api/editor/course', course.CourseAPIView.as_view(), name='course_api'),
    path('api/editor/course/list',
         course.CourseListAPIView.as_view(), name='course_list_api'),
    path('api/editor/course/<int:pk>',
         course.CourseEditAPIView.as_view(), name='course_edit_api'),
    path('api/editor/course/<int:pk>/delete',
         course.CourseDeleteAPIView.as_view(), name='course_delete_api'),

    # Lesson..................
    path('api/editor/course/lesson/create',
         lesson.LessonsListCreateAPIView.as_view(), name='lesson_create_api'),
    path('api/editor/course/lesson/<int:pk>',
         lesson.LessonsRetrieveUpdateDestroyAPIView.as_view(), name='lesson_edit_api'),
    path('api/editor/course/lesson/list',
         lesson.LessonsListAPIView.as_view(), name='lesson_list_api'),

    # ................

    # Course Request

    path('api/course/request/list', course.CourseRequestListAPIView.as_view(),
         name='course_request_list_api'),
    path('api/course/request/create', course.CourseRequestListCreateAPIView.as_view(),
         name='course_request_create_api'),
    path('api/editor/course/request/<int:pk>',
         course.CourseRequestRetrieveUpdateDestroyAPIView.as_view(), name='course_request_edit_api'),
    # --------


    # Notification
    path('api/editor/notification/create',
         Noti.NotificationListCreateAPIView.as_view(), name='notification_create_api'),

    path('api/editor/notification/list',
         Noti.NotificationListAPIView.as_view(), name='notification_list_api'),
     path('api/editor/device/list', Noti.UserDeviceListAPIView.as_view(),name="delvice_list_api"),

    path('api/editor/course/coursemenu/create',
         course.CourseMenuGroupListCreateAPIView.as_view(), name='course_menu_group_api'),
    path('api/editor/course/coursemenu/list',
         course.CourseMenuGroupListAPIView.as_view(), name='course_menu_group_list_api'),


    path('auth/login/', apiview.LoginView.as_view(), name='auth_user_login'),
    path('auth/register/', apiview.CreateUserApiView.as_view(),
         name='auth_user_create'),
    path('auth/changepassword/',
         apiview.UserChangePasswordView.as_view(), name='changepassword'),
    path('auth/forgotpassword/',
         apiview.ForgotPasswordView.as_view(), name='forgotpassword'),

    path('api/user/', apiview.UserApiView.as_view(), name='user'),

    path('api/courses/', apiview.CourseAPIView.as_view(), name='course_api'),
    path('api/courses/lessons/', apiview.LessonAPIView.as_view(), name='lesson_api'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
