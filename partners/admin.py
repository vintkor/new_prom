from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db import models
from .models import Provider, Region, Branch, File


class FileInline(admin.StackedInline):
    model = File
    extra = 0
    exclude = ['']


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        exclude = ['']


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_per_page = 25


class BranchInline(admin.StackedInline):
    extra = 0
    model = Branch
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple("Области", is_stacked=False)},
    }


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    pass


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    inlines = [FileInline, BranchInline]
