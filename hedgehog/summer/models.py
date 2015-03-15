# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import auth


# Create your models here.

class Lesson(models.Model):
    youtube_url = models.URLField()
    title = models.CharField(max_length=300)
    description = models.TextField()

    included_in_course = models.ForeignKey('Course', blank=False, related_name='lessons')
    number_in_course = models.IntegerField(db_index=True)

    link_to_homework = models.URLField(null=True)
    homework_commentary = models.TextField(blank=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/lessons/%d' % self.id

    class Meta:
        ordering = ['number_in_course']

class Course(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(default="")

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/courses/%d' % self.id


class Post(models.Model):
    pub_date = models.DateTimeField(db_index=True)
    description = models.TextField()

    def __unicode__(self):
        return self.description

    class Meta:
        ordering = ['-pub_date']

class MyUserManager(auth.models.BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        email = self.normalize_email(email)
        if not email:
            raise ValueError(r'У пользователя должен быть email')

        user = self.model(email=email,
                first_name=kwargs.get('first_name', ''), \
                last_name=kwargs.get('last_name', ''),
                grade=kwargs.get('grade', '7'),
                city=kwargs.get('city', ''))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.is_admin = True
        user.is_superuser = True
        return user

class User(auth.models.AbstractBaseUser):
    SEVENTH = '7'
    EIGHT = '8'
    NINTH = '9'
    TENTH = '10'
    GRADES_CHOICES = (
            (SEVENTH, 7), 
            (EIGHT, 8), 
            (NINTH, 9),
            (TENTH, 10)
        )

    first_name = models.CharField(max_length=30, verbose_name=r'Имя')
    last_name = models.CharField(max_length=30, verbose_name=r'Фамилия')
    email = models.EmailField(unique=True, db_index=True, verbose_name=r'Email')
    city = models.CharField(max_length=255, db_index=True, verbose_name=r'Город')
    grade = models.CharField(max_length=2, db_index=True, choices=GRADES_CHOICES,\
            verbose_name=r'Класс')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def __unicode__(self):
        return self.email

    class Meta:
        ordering = ['email']

    def get_absolute_url(self):
        return '/users/%d' % self.id
