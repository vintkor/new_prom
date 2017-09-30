from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db import models
from mptt.admin import DraggableMPTTAdmin
from .models import Category, Product, Feature, Delivery


class DeliveryInline(admin.StackedInline):
    extra = 0
    model = Delivery
    suit_classes = 'suit-tab suit-tab-delivery'


class FeatureInline(admin.TabularInline):
    extra = 0
    model = Feature
    suit_classes = 'suit-tab suit-tab-feature'


class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "active", "price", "step", "created", "updated"]
    list_filter = ["active", "category"]
    search_fields = ['title']
    inlines = [FeatureInline, DeliveryInline]
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple("Поставщики", is_stacked=False)},
    }
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-product',),
            'fields': ["title", "category", "price", "step", "text", "image", "active"]
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
