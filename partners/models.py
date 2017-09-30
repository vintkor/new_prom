from django.db import models
from new_prom.basemodel import BaseModel
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.crypto import get_random_string


def set_file_name(instance, filename):
    name = get_random_string(40)
    ext = filename.split('.')[-1]
    path = 'files/{}.{}'.format(name, ext)
    return path


class Region(BaseModel):
    title = models.CharField(verbose_name='Область', max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Область'
        verbose_name_plural = 'Области'


class Provider(BaseModel):
    title = models.CharField(verbose_name='Поставщик', max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'


class Branch(BaseModel):
    title = models.CharField(verbose_name='Филлиал', max_length=255)
    info = RichTextUploadingField(verbose_name='Информация о поставщике', default='', blank=True, null=True)
    parent_provider = models.ForeignKey(Provider, verbose_name='Поставщик', default=None, null=True, blank=True, on_delete=models.SET_NULL)
    region_for_work = models.ManyToManyField(Region, verbose_name='Область', related_name='Regions', default=None)

    def __str__(self):
        return "{}-{}".format(self.parent_provider, self.title)

    class Meta:
        verbose_name = 'Филлиал'
        verbose_name_plural = 'Филлиалы'


class File(BaseModel):
    provider = models.ForeignKey(Provider, verbose_name='Поставщик', default=None)
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    file = models.FileField(verbose_name='Файл', upload_to=set_file_name)

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        verbose_name = 'Прайс'
        verbose_name_plural = 'Прайсы'
