from reviews.models import Review
from django.forms import ModelForm
from users.forms import StyleMixin

class ReviewModelForm(StyleMixin,ModelForm):
    class Meta:
        model=Review
        fields=['rating','comment']
        