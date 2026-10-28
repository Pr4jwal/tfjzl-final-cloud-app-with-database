import sys
from django.utils.timezone import now

try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings
import uuid


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    # Many-to-many relationship between questions and lessons
    lessons = models.ManyToManyField(Lesson)

    question_text = models.TextField()
    grade = models.IntegerField(default=1)

    def is_get_score(self, selected_ids):
        """Checks whether the student selected all correct answers."""
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(
            is_correct=True,
            id__in=selected_ids
        ).count()

        selected_total = len(selected_ids)

        return (
            all_answers == selected_correct
            and selected_total == all_answers
        )

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)

    def __str__(self):
        return f"Submission {self.id} for Enrollment {self.enrollment.id}"
