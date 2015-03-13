from django.contrib import admin
from summer.models import MyUser, Lesson, Post, Course

class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'included_in_course', \
            'number_in_course']

# Register your models here.
admin.site.register(Post)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(MyUser)
admin.site.register(Course)
