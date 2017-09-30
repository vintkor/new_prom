from django.db import models
from new_prom.basemodel import BaseModel
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.crypto import get_random_string
from partners.models import Branch


def set_image_name(instance, filename):
    name = get_random_string(40)
    ext = filename.split('.')[-1]
    path = 'images/{}.{}'.format(name, ext)
    return path


def set_file_name(instance, filename):
    name = get_random_string(40)
    ext = filename.split('.')[-1]
    path = 'files/{}.{}'.format(name, ext)
    return path


class Category(BaseModel, MPTTModel):
    title = models.CharField(verbose_name='Категория', max_length=255)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    active = models.BooleanField(default=True, verbose_name="Вкл/Выкл")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return "{}".format(self.title)


class Product(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    category = TreeForeignKey(Category, blank=True, null=True)
    price = models.DecimalField(verbose_name="Цена", max_digits=8, decimal_places=2, blank=True, null=True)
    step = models.DecimalField(verbose_name="Шаг", max_digits=8, decimal_places=3, default=1)
    text = RichTextUploadingField(verbose_name="Текст поста", blank=True, default="")
    image = models.ImageField(verbose_name="Изображение", blank=True, default='', upload_to=set_image_name)
    active = models.BooleanField(default=True, verbose_name="Вкл/Выкл")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return "{}".format(self.title)


class Feature(BaseModel):
    product = models.ForeignKey(Product, verbose_name='Товар', default=None)
    title = models.CharField(verbose_name="Характеристика", max_length=150)
    file = models.FileField(verbose_name='Файл', upload_to=set_file_name, default=None, blank=True, null=True)
    text = RichTextUploadingField(verbose_name="Текст поста", blank=True, default="")

    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"

    def __str__(self):
        return "{}".format(self.title)


class Delivery(BaseModel):
    product = models.ForeignKey(Product, verbose_name="Товар")
    branch = models.ForeignKey(Branch, verbose_name="Филлиал")
    delivery = RichTextUploadingField(verbose_name="Доставка")
    delivery_my = RichTextUploadingField(verbose_name="Самовывоз")
    discount = RichTextUploadingField(verbose_name="Скидка")
    payment_cash = RichTextUploadingField(verbose_name="Оплата наличными")
    payment_card = RichTextUploadingField(verbose_name="Оплата картой")
    payment_bank = RichTextUploadingField(verbose_name="Оплата расчётный счёт")

    class Meta:
        verbose_name = "Доп инфо"
        verbose_name_plural = "Доп инфо"

    def __str__(self):
        return "{} - {}".format(self.product, self.branch)
