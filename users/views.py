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
        users = CustomUser.objects.filter(HR_link=request.user.pk)
        users_serializer = UserSerializer(users)
        data = users_serializer.data
        department = Department.objects.get(pk=data['department'])
        department_serializer = Departmenterializer(department)
        response = data
        response['department'] = department_serializer.data['name']
        return Response(response)


# class GetCurUserDataView(GenericAPIView):
#     serializer_class = UserSerializer
#     permission_classes = (IsAuthenticated,)
#
#     def get_queryset(self):
#         user = self.request.user
#         return user
#
#     def get(self,request,*args,**kwargs):
#         queryset = self.get_queryset()
#         serializer = self.serializer_class(queryset,*args,*kwargs)
#         return Response(serializer.data)



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



