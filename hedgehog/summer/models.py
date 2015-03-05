from django.db import models
from django.contrib import auth


# Create your models here.

class Lesson(models.Model):
    youtube_url = models.URLField()
    title = models.CharField(max_length=300)
    description = models.TextField()

    def __unicode__(self):
        return 'Lesson %s on %s' % (self.title, self.youtube_url)

class Post(models.Model):
    pub_date = models.DateTimeField(db_index=True)
    description = models.TextField()

    def __unicode__(self):
        return self.description

    class Meta:
        ordering = ['-pub_date']

class User(auth.models.User):
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

    city = models.CharField(max_length=255, db_index=True)
    grade = models.CharField(max_length=2, db_index=True, choices=GRADES_CHOICES)

    def set_password(self, psw):
        super(auth.models.User, self).set_password(psw)

    def __unicode__(self):
        return self.username

    class Meta:
        ordering = ['username']
