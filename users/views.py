from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ContactSerializer,UserSerializer, Departmenterializer
from .models import Contact,CustomUser, Department




class ContactViewSet(ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Contact.objects.all()


class GetCurUserDataView(APIView):
    def get(self, request):
        user = CustomUser.objects.get(pk=request.user.pk)
        users_serializer = UserSerializer(user)
        data = users_serializer.data
        department = Department.objects.get(pk=data['department'])
        department_serializer = Departmenterializer(department)
        response = data
        response['department'] = department_serializer.data['name']
        return Response(response)


class GetSuckersListView(APIView):
    def get(self, request):
        response = []
        if request.user.is_HR:
            HR_pk = request.user.pk
            users = CustomUser.objects.filter(HR_link=HR_pk)
            users_serializer = UserSerializer(users, many=True)
            for data in users_serializer.data:
                department = Department.objects.get(pk=data['department'])
                department_serializer = Departmenterializer(department)
                info = data
                info['department'] = department_serializer.data['name']
                response.append(info)
            return Response(response)



