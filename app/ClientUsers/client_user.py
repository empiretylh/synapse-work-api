from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import UserSerializer
from django.contrib.auth.models import User

class UserAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)