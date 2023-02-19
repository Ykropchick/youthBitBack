from rest_framework import serializers
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

class IntegerSerializer(serializers.Serializer):
    pk = serializers.IntegerField()


class NotificationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('pk', 'title', 'date', 'sender')

class NotificationRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('pk', 'title','description','sender','date')
