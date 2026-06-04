from django.db import models

# Create your models here.
from django.db import models
from courses.models import Course

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    order = models.IntegerField()
    is_free = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Homework(models.Model):
        lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE)
        title = models.CharField(max_length=255)
        description = models.TextField()


class Submission(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='submissions/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    admin_comment = models.TextField(blank=True, null=True)


class Progress(models.Model):
    student = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    is_completed = models.BooleanField(default=False)
    is_unlocked = models.BooleanField(default=False)

