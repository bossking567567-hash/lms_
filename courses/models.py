from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    order = models.IntegerField(default=0)
    is_free = models.BooleanField(default=False)

    def __str__(self):
        return self.title

from django.db import models
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)


    video_url = models.URLField(blank=True, null=True)


    file = models.FileField(upload_to='lessons/', blank=True, null=True)

    order = models.IntegerField(default=0)
    is_free = models.BooleanField(default=False)

    def __str__(self):
        return self.title