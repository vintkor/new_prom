from django import forms
from .models import Unit, Category


class SetCourseForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

    course = forms.CharField(label='Новый курс', widget=forms.NumberInput(
        attrs={'placeholder': 'Новый курс', 'step': '0.00001'},
    ))


class SetUnitForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), widget=forms.Select(), required=True)


class SetCategoryForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(), required=True)
