from django import forms
from blog.models import Blog
from users.forms import StyleFormMixin


class BlogForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания статьи в блоге"""
    class Meta:
        model = Blog
        exclude = ('is_published', 'views',)
