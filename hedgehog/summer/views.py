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
        name = 'Математика 7-8'
    elif name == 'phys78':
        name = 'Физика 7-8'
    elif name == 'math910':
        name = 'Математика 9-10'
    elif name == 'phys910':
        name = 'Физика 9-10'
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
            subject = 'Вопрос от %s' % form.cleaned_data['name'] 
            message = form.cleaned_data['question'] + '\n' + form.cleaned_data['email']
            sender = 'MSU-CHM@yandex.ru'

            recipients = ['misha@koltsov.su']
            send_mail(subject, message, sender, recipients)

            success(request, 'Сообщение успешно отправлено')
        else:
            error(request, form.subject.errors)

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

            username = email[:30]

            pswd = form.clean_password2()

            user = MyUser(username=username, first_name=first_name, last_name=last_name,\
                    city=city, grade=grade, password=pswd) 
            user.set_password(pswd)
            user.save()

            success(request, 'Вы успешно зарегистрированы')
        else:
            error(request, form.subject.errors)

        return redirect('/register/', permanent=True)

    else:
        form = MyUserCreationForm()

    return render(request, 'contact_us.html', {'form': form})
