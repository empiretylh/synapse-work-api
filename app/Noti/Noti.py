from rest_framework import generics
from ..models import Lessons, Notification, UserDevice
from ..serializers import LessonsSerializer, NotificationSerializer, UserDeviceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from .firebasenoti import send_multicast_message

class UserDeviceListAPIView(generics.ListAPIView):
    def get(self, request):
        queryset = UserDevice.objects.all()
        serializer = UserDeviceSerializer(queryset, many=True)
        return Response(serializer.data)


class NotificationListCreateAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user.is_admin or request.user.is_editor:
            serializer = NotificationSerializer(data=request.data)

            if serializer.is_valid():
                print(serializer.validated_data)
                serializer.save()

                sended_device = request.data.get('sended_device')
                title = request.data.get('title')
                message = request.data.get('message')
                action_url = request.data.get('action_url')


                fcm_tokens = []

                for id in sended_device:
                    userdv = UserDevice.objects.get(id=id)
                    fcm_tokens.append(userdv.fcm_token)

                data = {
                    "url" : action_url
                }


                # print(fcm_tokens)
                send_multicast_message(fcm_tokens,title, message, data)

                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            raise PermissionDenied()


class NotificationListAPIView(APIView):
    def get(self, request):
        notification_id = request.query_params.get('id')

        
        if notification_id:
            queryset = Notification.objects.filter(id=notification_id)
        else:
            user_devices = UserDevice.objects.filter(user=request.user)
            queryset = Notification.objects.filter(sended_device__in=user_devices)



        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data)