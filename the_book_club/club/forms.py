from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserCreationForm(forms.UserCreationForm):
    username = forms.CharField(label='имя пользователя')
    password1 = forms.CharField(label='пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='подтверждение пароля', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        labels = {
            'username': 'Имя пользователя',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }

    