from django.contrib import admin, messages
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db import models
from mptt.admin import DraggableMPTTAdmin
from .models import Category, Product, Feature, Delivery, Unit
from import_export import resources
from jet.admin import CompactInline
from jet.filters import DateRangeFilter
from .forms import SetCourseForm, SetUnitForm, SetCategoryForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from xlsxwriter import Workbook
from django.http import HttpResponse
import datetime


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_title', 'created')


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product


class DeliveryInline(CompactInline):
    extra = 0
    model = Delivery
    suit_classes = 'suit-tab suit-tab-delivery'


class FeatureInline(CompactInline):
    extra = 0
    model = Feature
    suit_classes = 'suit-tab suit-tab-feature'


def re_count_on(modeladmin, request, queryset):
    for item in queryset:
        item.re_count = True
        item.save(update_fields=('re_count',))


re_count_on.short_description = 'Пересчитывать в грн'


def re_count_off(modeladmin, request, queryset):
    for item in queryset:
        item.re_count = False
        item.save(update_fields=('re_count',))


re_count_off.short_description = 'Не пересчитывать в грн'


def set_course(modeladmin, request, queryset):
    form = None
    template = 'set-course.html'
    context = {'items': queryset, 'title': 'Установыть новый курс', 'action': 'set_course'}

    if 'apply' in request.POST:
        form = SetCourseForm(request.POST)

        if form.is_valid():
            course = form.cleaned_data['course']

            count = 0
            for item in queryset:
                item.course = course
                item.save()
                count += 1

            modeladmin.message_user(request, "Курс {} установлен у {} товаров.".format(course, count), level=messages.SUCCESS)
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = SetCourseForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        context['form'] = form

    return render(request, template, context)


set_course.short_description = 'Установить новый курс'


def set_unit(modeladmin, request, queryset):
    form = None
    template = 'set-course.html'
    context = {'items': queryset, 'title': 'Установить единицу измерения', 'action': 'set_unit'}

    if 'apply' in request.POST:
        form = SetUnitForm(request.POST)

        if form.is_valid():
            unit = form.cleaned_data['unit']

            count = 0
            for item in queryset:
                item.unit = unit
                item.save()
                count += 1

            modeladmin.message_user(request, "Единица измерения '{}' установлена у {} товаров.".format(unit, count),
                                    level=messages.SUCCESS)
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = SetUnitForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        context['form'] = form

    return render(request, template, context)


set_unit.short_description = 'Установить единицу измерения'


def set_category(modeladmin, request, queryset):
    form = None
    template = 'set-course.html'
    context = {'items': queryset, 'title': 'Установить категорию', 'action': 'set_category'}

    if 'apply' in request.POST:
        form = SetCategoryForm(request.POST)

        if form.is_valid():
            category = form.cleaned_data['category']

            count = 0
            for item in queryset:
                item.category = category
                item.save()
                count += 1

            modeladmin.message_user(request, "Категория '{}' установлена у {} товаров.".format(category, count),
                                    level=messages.SUCCESS)
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = SetCategoryForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        context['form'] = form

    return render(request, template, context)


set_category.short_description = 'Установить категорию'


def save_as_xlsx(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/xlsx')
    response['Content-Disposition'] = 'attachment; filename="ppf-catalog-{}.xlsx"'.format(datetime.datetime.now())

    workbook = Workbook(response)
    worksheet = workbook.add_worksheet('Export Products Sheet')

    header = (
        'Название_позиции',
        'Ключевые_слова',
        'Описание',
        'Тип_товара',
        'Цена',
        'Валюта',
        'Единица_измерения',
        'Ссылка_изображения',
        'Наличие',
        'Идентификатор_товара',
        'Идентификатор_группы',
        'Код_товара',
    )

    [worksheet.write(0, col, i) for col, i in enumerate(header)]

    for row, item in enumerate(queryset):
        worksheet.write(row + 1, 0, item.title)
        worksheet.write(row + 1, 1, item.category.title)
        worksheet.write(row + 1, 2, item.text)
        worksheet.write(row + 1, 3, 'r')
        worksheet.write(row + 1, 4, item.get_price_UAH())
        worksheet.write(row + 1, 5, item.get_currency_code())
        worksheet.write(row + 1, 6, item.unit.short_title)
        worksheet.write(row + 1, 7, 'http://{}{}'.format(request.META.get('HTTP_HOST'), item.image.url))
        worksheet.write(row + 1, 8, '+')
        worksheet.write(row + 1, 9, item.code)
        worksheet.write(row + 1, 10, item.category.id)
        worksheet.write(row + 1, 11, item.code)

    return response


save_as_xlsx.short_description = 'Сохранить в формате XLSX'


class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "code", "active", "price", "get_currency_code", "course",
                    "re_count", "get_price_UAH", "unit", "step", "updated")
    list_filter = (('created', DateRangeFilter), 'code', 'category', 'currency', 're_count')
    readonly_fields = ["code"]
    search_fields = ('title',)
    resource_class = ProductResource
    inlines = (FeatureInline, DeliveryInline)
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple("Поставщики", is_stacked=False)},
    }
    actions = (set_category, set_course, set_unit, re_count_off, re_count_on, save_as_xlsx)


admin.site.register(Product, ProductAdmin)
admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=('tree_actions', 'indented_title', 'active'),
    list_display_links=('indented_title',),
)
