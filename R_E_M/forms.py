from django import forms
from R_E_M.models import Blog


class BlogModelForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'category', 'image', 'alt_text', 'youtube']
