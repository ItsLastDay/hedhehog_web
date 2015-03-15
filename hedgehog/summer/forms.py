# -*- coding: utf-8 -*-
from django import forms
from summer.models import User

class HomeworkSubmitForm(forms.Form):
    file = forms.FileField()

class ContactForm(forms.Form):
    email = forms.EmailField(label=r'Ваш e-mail')
    name = forms.CharField(label=r'Ваше имя', max_length=100)
    question = forms.CharField(widget=forms.Textarea, label=r'Ваше сообщение')

class MyUserCreationForm(forms.Form):
    email = forms.EmailField(label='E-mail', required=True)
    first_name = forms.CharField(max_length=255, label=r'Имя')
    last_name = forms.CharField(max_length=255, label=r'Фамилия', required=True)

    city = forms.CharField(max_length=255, label=r'Город')
    grade = forms.ChoiceField(label=r'Класс', choices=User.GRADES_CHOICES, required=True)

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput())

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(r'Введённые пароли не совпадают')
        return password1


    def clean_email(self):
        username = self.cleaned_data['email']
        try:
            User.objects.get(email=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(r'Такой пользователь уже существует')
