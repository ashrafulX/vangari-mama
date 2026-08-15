from django import forms
from users.forms import StyleMixin
from listings.models import Category,Listing


class CreateCategoryModelForm(StyleMixin,forms.ModelForm):
    class Meta:
        model=Category
        fields=['name']

    


class ListingCreateModelForm(StyleMixin, forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'quantity', 'image', 'category','status']
        labels = {
            'price': 'Price (TK)',
            'quantity': 'Quantity (KG)',
        }