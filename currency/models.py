from django.db import models
from new_prom.basemodel import BaseModel


class Currency(BaseModel):
    title = models.CharField(max_length=100, verbose_name='Название')
    code = models.CharField(max_length=3, verbose_name='Код валюты')
    active = models.BooleanField(default=True, verbose_name='Активная')

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Вылюты'

    def __str__(self):
        return self.title
