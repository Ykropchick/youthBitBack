from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from rest_framework.response import Response

from users.models import CustomUser as User
from users.serializers import UserSerializer

from .serializers import NotificationListSerializer, NotificationRetrieveSerializer
from .models import Notification


class NotificationListView(APIView):
    def get(self, request):
        response = []
        user = self.request.user
        notifications = Notification.objects.filter(to=user)
        notifications_serializer = NotificationListSerializer(notifications, many=True)
        for data in notifications_serializer.data:
            info = data

            user = User.objects.get(pk=data['sender'])
            user_serializer = UserSerializer(user)
            info['sender'] = user_serializer.data['firstname'] + " " + user_serializer.data['lastname']
            response.append(info)



        return Response(response)


class NotificationDetailView(APIView):
    def get(self, request, pk):
        response = {}
        user = self.request.user
        notifications = Notification.objects.filter(pk=pk)
        notifications_serializer = NotificationRetrieveSerializer(notifications, many=True)
        user = User.objects.get(pk=notifications_serializer.data[0]['sender'])
        user_serializer = UserSerializer(user)
        response = notifications_serializer.data[0]
        response['sender'] = user_serializer.data['firstname'] + " " + user_serializer.data['lastname']
        return Response(response)




