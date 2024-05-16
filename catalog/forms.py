from django import forms
from django.forms import BooleanField

from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):

    forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    class Meta:
        model = Product
        fields = ('name', 'category', 'price', 'description', 'preview')

    def clean_name(self):
        cleaned_data = self.cleaned_data['name'].lower()

        for word in self.forbidden_words:
            if word in cleaned_data:
                raise forms.ValidationError(f'Вы использовали запрещенне слово {word}')

        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description'].lower()

        for word in self.forbidden_words:
            if word in cleaned_data:
                raise forms.ValidationError(f'Вы использовали запрещенное слово {word}')

        return cleaned_data


class ProductModeratorForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Product
        fields = ('category', 'description', 'is_published',)


class VersionForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Version
        fields = "__all__"
