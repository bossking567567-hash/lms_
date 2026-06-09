from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Submission, Progress

@receiver(post_save, sender=Submission)
def auto_unlock_lesson(sender, instance, created, **kwargs):
    """
    Submission approved bo‘lsa lesson unlock bo‘ladi
    """

    if instance.status != "approved":
        return

    lesson = instance.homework.lesson

    Progress.objects.update_or_create(
        student=instance.student,
        lesson=lesson,
        defaults={
            "is_completed": True,
            "is_unlocked": True
        }
    )