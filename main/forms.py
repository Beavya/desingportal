from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re
from django.contrib.auth.forms import AuthenticationForm
from .models import Application

class UserRegisterForm(UserCreationForm):
    last_name = forms.CharField(max_length=100, label='Фамилия')
    first_name = forms.CharField(max_length=100, label='Имя')
    patronymic = forms.CharField(max_length=100, label='Отчество', required=False)
    agree = forms.BooleanField(label='Согласие на обработку персональных данных')

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'patronymic', 'username', 'email', 'password1', 'password2', 'agree']

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^[а-яА-ЯёЁ\s\-]+$', last_name):
            raise forms.ValidationError("Фамилия должна содержать только буквы кириллицы, дефис и пробелы")
        return last_name

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[а-яА-ЯёЁ\s\-]+$', first_name):
            raise forms.ValidationError("Имя должно содержать только буквы кириллицы, дефис и пробелы")
        return first_name

    def clean_patronymic(self):
        patronymic = self.cleaned_data.get('patronymic')
        if patronymic and not re.match(r'^[а-яА-ЯёЁ\s\-]+$', patronymic):
            raise forms.ValidationError("Отчество должно содержать только буквы кириллицы, дефис и пробелы")
        return patronymic

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z\-]+$', username):
            raise forms.ValidationError("Логин должен содержать только латиницу и дефис")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Этот логин уже занят")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже используется")
        return email

    def clean_agree(self):
        agree = self.cleaned_data.get('agree')
        if not agree:
            raise forms.ValidationError("Необходимо согласие на обработку персональных данных")
        return agree

    def save(self, commit=True):
        user = super().save(commit=False)
        user.last_name = self.cleaned_data['last_name']
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    pass

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['title', 'description', 'category', 'image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            ext = image.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'bmp']:
                raise forms.ValidationError('Разрешены только jpg, jpeg, png, bmp')
            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Размер файла не более 2MB')
        return image