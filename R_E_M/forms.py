from django import forms
from R_E_M.models import Blog
from martor.fields import MartorFormField


class BlogModelForm(forms.ModelForm):
    content = MartorFormField()
    class Meta:
        model = Blog
        fields = ['title', 'content', 'category', 'image', 'alt_text', 'youtube']
