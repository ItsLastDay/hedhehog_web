from django import forms
from summer.models import MyUser

class HomeworkSubmitForm(forms.Form):
    file = forms.FileField()

class ContactForm(forms.Form):
    email = forms.EmailField(label='Ваш e-mail')
    name = forms.CharField(label='Ваше имя', max_length=100)
    question = forms.CharField(widget=forms.Textarea, label='Ваше сообщение')

class MyUserCreationForm(forms.Form):
    email = forms.EmailField(label='E-mail')
    first_name = forms.CharField(max_length=255, label='Имя')
    last_name = forms.CharField(max_length=255, label='Фамилия')

    city = forms.CharField(max_length=255, label='Город')
    grade = forms.ChoiceField(label='Класс', choices=MyUser.GRADES_CHOICES)

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput())

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Введённые пароли не совпадают.')

