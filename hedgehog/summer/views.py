# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.contrib.messages import error, success
from django.views.decorators.http import require_GET, require_POST

from summer.models import *
from summer.forms import *

# Create your views here.

@require_GET
def main_page(request):
    return render(request, 'base.html', dict())

@require_GET
def video_lesson_page(request, v_id):
    data = dict()

    try:
        video = Lesson.objects.prefetch_related('included_in_course__lessons').get(id=v_id)
        course = video.included_in_course
    except:
        error(request, 'Запрошенный урок не найден')
        return redirect("/lectures/all", permanent=True)

    data['course'] = course
    data['video'] = video
    data['other_lessons'] = course.lessons.all()

    if request.method == "POST":
        form = HomeworkSubmitForm(request.POST, request.FILES)
        if form.is_valid():
            return redirect("", permanent=True)
    else:
        form = HomeworkSubmitForm()

    data['form'] = form

    return render(request, 'videolesson.html', data)

@require_GET
def video_lectures_all(request):
    data = dict()

    try:
        courses = Course.objects.prefetch_related('lessons').all()
    except:
        return render(request, 'allvideo.html', {'error_message': 'Невозможно запросить курсы из базы данных'})

    data['courses'] = courses

    return render(request, 'allvideo.html', data)

@require_GET
def specific_course(request, name):
    if name == 'math78':
        name = u'Математика 7-8'
    elif name == 'phys78':
        name = u'Физика 7-8'
    elif name == 'math910':
        name = u'Математика 9-10'
    elif name == 'phys910':
        name = u'Физика 9-10'
    else:
        return redirect('/lectures/all', permanent=True)

    data = dict()

    course = Course.objects.prefetch_related('lessons').get(name=name)

    data['course'] = course

    return render(request, 'course_with_description.html', data)


@require_GET
def teachers(request):
    return render(request, 'teachers.html')

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            subject = u'Вопрос от %s' % form.cleaned_data['name'] 
            message = form.cleaned_data['question'] + '\n' + form.cleaned_data['email']
            sender = 'MSU-CHM@yandex.ru'

            recipients = ['misha@koltsov.su']
            send_mail(subject, message, sender, recipients)

            success(request, u'Сообщение успешно отправлено')
        else:
            error(request, form.errors)

        return redirect('/contacts', permanent=True)
    else:
        form = ContactForm()

    return render(request, 'contact_us.html', {'form': form})

def registration_view(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            city = form.cleaned_data['city']
            grade = form.cleaned_data['grade']

            pswd = form.clean_password2()

            user = MyUser.objects.create_user(email,\
                    pswd, \
                    first_name=first_name, last_name=last_name,\
                    city=city, grade=grade) 
            user.save()

            success(request, u'Вы успешно зарегистрированы')
        else:
            error(request, form.errors)

        return redirect('/register/', permanent=True)

    else:
        form = MyUserCreationForm()

    return render(request, 'register.html', {'form': form})

def user_view(request, uid):
    try:
        user = MyUser.objects.get(id=uid)
    except:
        error(request, u'Запрошенный пользователь не найден.')
        return redirect('/home/', permanent=True)

    return render(request, 'userpage.html', {'user_r': user})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            success(request, 'Вход успешно произведен')
            return redirect('/home/', permanent=True)
        else:
            error(request, 'Неверный e-mail или пароль')
            return redirect('/login/', permanent=True)
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/home', permanent=True)

def not_found(request):
    error(request, 'Запрашиваемая вами страница не найдена')
    return redirect('/home', permanent=True)
