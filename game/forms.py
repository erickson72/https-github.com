from django import forms
from .models import*

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name',)
        #fields = ('category_name', 'birthdate', 'country', 'city')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category_name'].queryset = Category.objects.none()


class AnswersForm(forms.Form):
    answer = forms.CharField(max_length=100)
