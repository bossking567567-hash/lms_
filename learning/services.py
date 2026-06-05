from .models import Submission, Homework, Lesson, Progress


def can_unlock_next_lesson(student, lesson):
    homework = Homework.objects.filter(lesson=lesson).first()

    if not homework:
        return True

    submission = Submission.objects.filter(
        homework=homework,
        student=student,
        status='approved'
    ).first()

    return submission is not None

from .models import Submission, Homework, Lesson


def is_lesson_unlocked(student, lesson):

    if lesson.order == 1:
        return True

    prev_lesson = Lesson.objects.filter(
        course=lesson.course,
        order=lesson.order - 1
    ).first()

    if not prev_lesson:
        return True

    homework = Homework.objects.filter(lesson=prev_lesson).first()
    if not homework:
        return True

    submission = Submission.objects.filter(
        homework=homework,
        student=student,
        status='approved'
    ).exists()

    return submission


from .models import Progress


def mark_progress(student, lesson):
    obj, created = Progress.objects.get_or_create(
        student=student,
        lesson=lesson
    )
    obj.is_completed = True
    obj.save()