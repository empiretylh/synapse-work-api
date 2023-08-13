from django.urls import path, include

# from app.models import SalesTwoDigits
from . import views
from . import apiview
from django.conf.urls.static import static
from django.conf import settings


from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [



    path('auth/login/', apiview.LoginView.as_view(), name='auth_user_login'),
    path('auth/register/', apiview.CreateUserApiView.as_view(),
         name='auth_user_create'),
    path('auth/changepassword/',apiview.UserChangePasswordView.as_view(),name='changepassword'),
    path('auth/forgotpassword/',apiview.ForgotPasswordView.as_view(),name='forgotpassword'),

    path('api/user/',apiview.UserApiView.as_view(),name='user'),

    path('api/courses/',apiview.CourseAPIView.as_view(),name='course_api'),
    path('api/courses/lessons/',apiview.LessonAPIView.as_view(),name='lesson_api'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
