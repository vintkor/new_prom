from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db import models
from mptt.admin import DraggableMPTTAdmin
from .models import Category, Product, Feature, Delivery
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from jet.admin import CompactInline
from jet.filters import DateRangeFilter


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


class ProductAdmin(ImportExportActionModelAdmin):
    list_display = ["title", "category", "code", "active", "price", "step", "created", "updated"]
    list_filter = (('created', DateRangeFilter), 'category', )
    readonly_fields = ["code"]
    search_fields = ['title']
    resource_class = ProductResource
    inlines = [FeatureInline, DeliveryInline]
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple("Поставщики", is_stacked=False)},
    }
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-product',),
            'fields': ["title", "category", "code", "price", "step", "text", "image", "active"]
        }),
    ]
    suit_form_tabs = (
        ('product', 'Товар'),
        ('feature', 'Характеристики'),
        ('delivery', 'Доп инфо'),
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=('tree_actions', 'indented_title', 'active'),
    list_display_links=('indented_title',),
)
