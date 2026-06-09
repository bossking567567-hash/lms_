from .models import Homework, Submission, Progress

def is_lesson_unlocked(user, lesson):
    """
    Lesson ochiqmi yoki yo‘qmi tekshiradi
    """


    if lesson.is_free:
        return True


    homework = Homework.objects.filter(lesson=lesson).first()

    if not homework:
        return True


    return Submission.objects.filter(
        homework=homework,
        student=user,
        status='approved'
    ).exists()

def unlock_lesson(user, lesson):
    """
    Lesson ochilganda progress yoziladi
    """

    Progress.objects.update_or_create(
        student=user,
        lesson=lesson,
        defaults={
            "is_completed": True,
            "is_unlocked": True
        }
    )

from .models import Enrollment


def is_enrolled(user, course):
    return Enrollment.objects.filter(
        student=user,
        course=course
    ).exists()

from .models import Progress
from courses.models import Lesson


def get_next_lesson(course, current_lesson):
    return Lesson.objects.filter(
        course=course,
        order__gt=current_lesson.order
    ).order_by('order').first()

def unlock_lesson(student, lesson):
    Progress.objects.update_or_create(
        student=student,
        lesson=lesson,
        defaults={
            "is_unlocked": True,
            "is_completed": True
        }
    )

from courses.models import Lesson
from .models import Progress


def get_course_progress(user, course):
    lessons = Lesson.objects.filter(course=course)
    total = lessons.count()

    completed = Progress.objects.filter(
        student=user,
        lesson__course=course,
        is_completed=True
    ).count()

    if total == 0:
        return 0

    return int((completed / total) * 100)

def is_course_completed(user, course):
    return get_course_progress(user, course) == 100

