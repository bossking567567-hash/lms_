from django.db import models
from django.conf import settings
from courses.models import Lesson


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

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    answer_text = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='submissions/', blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS, default='pending')


class Progress(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    is_completed = models.BooleanField(default=False)
    is_unlocked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'lesson')

from django.db import models
from django.conf import settings
from courses.models import Course


class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} -> {self.course}"