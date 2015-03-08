from django.contrib import admin
from summer.models import User, Lesson, Post

# Register your models here.
admin.site.register(Post)
admin.site.register(Lesson)
admin.site.register(User)
