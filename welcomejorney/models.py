from django.db import models
from users.models import Department


class Module(models.Model):
    name = models.CharField('Название',max_length=100)
    description = models.CharField('Описание', max_length=300,null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL,
null=True, verbose_name='Отдел')

class Manual(models.Model):
    name = models.CharField('Название',max_length=60)
    description = models.CharField('Описание',max_length=100)
    link = models.FileField('ссылка на документ',upload_to='manuals')
    module = models.ForeignKey(Module,on_delete=models.CASCADE,verbose_name='Модуль')

