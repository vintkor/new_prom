from django.contrib import admin, messages
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db import models
from mptt.admin import DraggableMPTTAdmin
from .models import Category, Product, Feature, Delivery
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from jet.admin import CompactInline
from jet.filters import DateRangeFilter
from .forms import SetCourseForm
from django.http import HttpResponseRedirect
from django.shortcuts import render


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
    context = {'items': queryset, 'title': 'Установыть новый курс'}

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


class ProductAdmin(ImportExportActionModelAdmin):
    list_display = ("title", "category", "code", "active", "price", "get_currency_code", "course",
                    "re_count", "get_price_UAH", "step", "created", "updated")
    list_filter = (('created', DateRangeFilter), 'code', 'category', 'currency', 're_count')
    readonly_fields = ["code"]
    search_fields = ('title',)
    resource_class = ProductResource
    inlines = (FeatureInline, DeliveryInline)
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple("Поставщики", is_stacked=False)},
    }
    actions = (set_course, re_count_off, re_count_on)


admin.site.register(Product, ProductAdmin)
admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=('tree_actions', 'indented_title', 'active'),
    list_display_links=('indented_title',),
)
