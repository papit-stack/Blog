from django import forms
from .models import Blog,Comment

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
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your comment here...',
                'class': 'form-control'
            }),
        }
        labels = {
            'content': '',
        }