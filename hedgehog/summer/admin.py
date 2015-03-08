from django.contrib import admin
from summer.models import User, Lesson, Post, Course

class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'included_in_course', \
            'number_in_course']

# Register your models here.
admin.site.register(Post)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(User)
admin.site.register(Course)
