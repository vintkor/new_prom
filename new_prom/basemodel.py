from django.db import models
from django.utils.translation import ugettext as _


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Создание')
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name='Обновление')

    objects = models.Manager()