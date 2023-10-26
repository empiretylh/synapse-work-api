from rest_framework import generics
from ..models import Lessons
from ..serializers import LessonsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

       
class IsCourseCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user or request.user.is_admin

class LessonsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
    # user is editor or admin
    permission_classes = [permissions.IsAuthenticated, IsCourseCreator]

    def perform_create(self, serializer):
        
        user = self.request.user
        if user.is_admin:
            serializer.save()
        elif user.is_editor:
            serializer.save(user=user)
        else:
            raise PermissionDenied("You don't have permission to create a course.")

class LessonsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer


class LessonsListAPIView(APIView):
    def get(self, request):
        lesson_id = request.query_params.get('lesson_id')
        course_menu_id = request.query_params.get('coursemenu_id')
        if lesson_id:
            queryset = Lessons.objects.filter(id=lesson_id)
        elif course_menu_id:
            queryset = Lessons.objects.filter(course_menu__id=course_menu_id)
        elif lesson_id and course_menu_id:
            queryset = Lessons.objects.filter(id=lesson_id,course_menu__id=course_menu_id)
        else:
            queryset = Lessons.objects.all()

        serializer = LessonsSerializer(queryset, many=True)
        return Response(serializer.data)