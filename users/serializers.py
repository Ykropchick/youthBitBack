from rest_framework.serializers import ModelSerializer

from .models import Contact,CustomUser, Department
class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"

class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('pk', 'firstname', 'lastname', 'email', 'department', 'position', 'is_HR')

class Departmenterializer(ModelSerializer):
    class Meta:
        model = Department
        fields = ('__all__')