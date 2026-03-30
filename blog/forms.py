from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Заголовок поста'}),
            'content': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Содержимое поста...'}),
            'category': forms.Select(),
            'image': forms.FileInput(),
            'status': forms.Select(),
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise ValidationError('Заголовок обязателен')
        return title