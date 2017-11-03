from django import forms


class SetCourseForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

    course = forms.CharField(label='Новый курс', widget=forms.NumberInput(
        attrs={'placeholder': 'Новый курс', 'step': '0.00001'},
    ))
