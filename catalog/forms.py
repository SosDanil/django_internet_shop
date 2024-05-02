from django import forms

from catalog.models import Product


class ProductForm(forms.ModelForm):

    forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    class Meta:
        model = Product
        fields = ('name', 'category', 'price', 'description', 'preview')

    def clean_name(self):
        cleaned_data = self.cleaned_data['name'].lower()

        for word in self.forbidden_words:
            if word in cleaned_data:
                raise forms.ValidationError('Вы использовали запрещенные слова')

        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']

        for word in self.forbidden_words:
            if word in cleaned_data:
                raise forms.ValidationError('Вы использовали запрещенные слова')

        return cleaned_data
