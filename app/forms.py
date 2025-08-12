from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = [
            'blog_title',
            'category',
            'blog_short_description',
            'blog_description',
            'image',
            'status',
        ]

        widgets = {
            'blog_short_description': forms.Textarea(attrs={'rows': 3}),
            'blog_description': forms.Textarea(attrs={'rows': 6}),
            'slug': forms.TextInput(attrs={'placeholder': 'auto-generated or custom'}),
        }