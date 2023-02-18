from django.http import HttpResponse
from rest_framework.generics import GenericAPIView

from users.models import Department
from django.contrib.auth import get_user_model
from random import randint,choice

class FillView(GenericAPIView):
    def get(self,*args,**kwargs):
        department = Department.objects.create(name='testdep', head='test_head',
place='zalupa')

        users = []
        user_model = get_user_model()
        for i in range(10):
            email = f'test{i}@test.com'
            password = 'Qwerty123321'
            firstname = 'test'
            lastname = 'user'
            is_HR = randint(0, 1)
            if not is_HR:
                HR_link = choice(list(user_model.objects.filter(is_HR=True))).pk

            user_model.objects.create_user(email=email,
                                           password=password, firstname=firstname, lastname=lastname, is_HR=is_HR)

        return HttpResponse("Готово")