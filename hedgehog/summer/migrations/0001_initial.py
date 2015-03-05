# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('youtube_url', models.URLField()),
                ('title', models.CharField(max_length=300)),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('pub_date', models.DateTimeField(db_index=True)),
                ('description', models.TextField()),
            ],
            options={
                'ordering': ['-pub_date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, to=settings.AUTH_USER_MODEL, primary_key=True, auto_created=True, serialize=False)),
                ('city', models.CharField(max_length=255, db_index=True)),
                ('grade', models.CharField(max_length=2, choices=[('7', 7), ('8', 8), ('9', 9), ('10', 10)], db_index=True)),
            ],
            options={
                'ordering': ['username'],
            },
            bases=('auth.user',),
        ),
    ]
