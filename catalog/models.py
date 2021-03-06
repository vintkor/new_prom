from django.db import models
from new_prom.basemodel import BaseModel
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.crypto import get_random_string
from partners.models import Branch
from django.core.urlresolvers import reverse
from currency.models import Currency


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


def set_code():
    last_product = Product.objects.first()
    if last_product is None:
        new_code = 'ПФ-10000'
    else:
        last_code = last_product.code.split('-')
        new_code = '{}-{}'.format(last_code[0], (int(last_code[1]) + 1))
    return new_code


class Unit(BaseModel):
    title = models.CharField(max_length=200, verbose_name='Название')
    short_title = models.CharField(max_length=10, verbose_name='Короткое обозначение')

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'
        ordering = ('title',)

    def __str__(self):
        return self.short_title


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

    def get_absolute_url(self):
        return reverse('category', args=[self.id])

    def get_id(self):
        if self.parent:
            return self.parent.id
        return ''


class Product(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    category = TreeForeignKey(Category, blank=True, null=True, verbose_name='Категория')
    price = models.DecimalField(verbose_name="Цена", max_digits=8, decimal_places=2, blank=True, null=True)
    currency = models.ForeignKey(Currency, null=True, blank=True, default=None)
    course = models.DecimalField(verbose_name='Курс', max_digits=12, decimal_places=5, blank=True, null=True, default=1)
    re_count = models.BooleanField(verbose_name="Пересчитывать в грн?", default=True)
    unit = models.ForeignKey(Unit, verbose_name='Единица измерения', blank=True, null=True, default=None)
    step = models.DecimalField(verbose_name="Шаг", max_digits=8, decimal_places=3, default=1)
    text = RichTextUploadingField(verbose_name="Текст поста", blank=True, default="")
    image = models.ImageField(verbose_name="Изображение", blank=True, default='', upload_to=set_image_name)
    active = models.BooleanField(default=True, verbose_name="Вкл/Выкл")
    code = models.CharField(verbose_name="Артикул", max_length=20, default=set_code, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ('-code',)

    def __str__(self):
        return "{}".format(self.title)

    def get_absolute_url(self):
        return reverse('single-product', args=[str(self.id)])

    def get_currency_code(self):
        if self.currency:
            if self.re_count:
                return Currency.objects.get(code='UAH').code
            return self.currency.code
        return None
    get_currency_code.short_description = 'Валюта'

    def get_price_UAH(self):
        if self.price:
            if self.re_count:
                return round(self.price * self.course, 3)
            else:
                return round(self.price, 3)
        return False
    get_price_UAH.short_description = 'Цена в валюте'

    def get_delivery_count(self):
        return self.delivery_set.count()

    def get_unit(self):
        if self.unit:
            return self.unit.short_title
        return 'шт.'

    def get_images_count(self):
        return Photo.objects.filter(product=self).count()

    get_images_count.short_description = 'Доп изобр.'

    def get_all_photo(self):
        images = list()
        other_photo = Photo.objects.filter(product=self)

        if self.image:
            images.append(self.image.url)

        for item in other_photo:
            images.append(item.image.url)

        return images

    def get_images(self):
        return Photo.objects.filter(product=self)


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
    delivery_condition = RichTextUploadingField(verbose_name="Условие поставки", default=' ')
    return_product = RichTextUploadingField(verbose_name="Возврат", blank=True, null=True, default=None)

    class Meta:
        verbose_name = "Доп инфо"
        verbose_name_plural = "Доп инфо"

    def __str__(self):
        return "{} - {}".format(self.product, self.branch)


class Photo(BaseModel):
    product = models.ForeignKey(Product, verbose_name='Товар')
    image = models.ImageField(verbose_name='Изображение', upload_to=set_image_name)
    weight = models.PositiveSmallIntegerField(verbose_name='Порядок', default=0)

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"
        ordering = ['weight']

    def __str__(self):
        return "Image to product {}".format(self.product)

    def get_img_tag(self):
        return """<span style="
                                background-image: url('{}');
                                background-size: cover;
                                background-position: center;
                                width: 60px; height: 40px;
                                display: block;
                                position: relative;
                                "><span>""".format(self.image.url)

    get_img_tag.short_description = 'Preview'
    get_img_tag.allow_tags = True
