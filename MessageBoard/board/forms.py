from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Post, Comment
from django import forms
from django.contrib.auth.forms import UserCreationForm


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'category', 'title', 'text', 'img', 'video']
        widgets = {
            'author': forms.Select(attrs={
                'class': 'form-control',
            }),
            'category': forms.SelectMultiple(attrs={
                'class': 'form-control',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'img': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'video': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            })
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['commentPost', 'commentUser', 'text']
        widgets = {
            'commentPost': forms.Select(attrs={
                'class': 'form-control',
            }),
            'commentUser': forms.Select(attrs={
                'class': 'form-control',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control'
            }),
        }


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label='Password')
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label='Confirm Password')

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return super().clean()
