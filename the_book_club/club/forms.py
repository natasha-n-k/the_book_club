from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

from django.contrib.auth.models import User
from .models import Book, BookClub, Meeting

class ClubAdminForm(forms.Form):
    book = forms.ModelChoiceField(queryset=Book.objects.all(), label='Книга для чтения')
    meeting_date = forms.DateField(label='Дата встречи', widget=forms.DateInput(format='%d.%m.%Y'), input_formats=('%d.%m.%Y',))
    meeting_location = forms.CharField(label='Место встречи')

class UserCreationForm(BaseUserCreationForm):
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

    
