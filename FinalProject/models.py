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

    question_text = models.CharField(max_length=500)
    question_point = models.IntegerField(default=1)

    def is_get_score(self, selected_ids):
        """Checks if the student selected all the correct answers."""
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(
            is_correct=True,
            id__in=selected_ids
        ).count()

        selected_total = len(selected_ids)

        if all_answers == selected_correct and selected_total == all_answers:
            return True
        else:
            return False

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    # One-to-many relationship between Question and Choice
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    # One enrollment can have multiple submissions
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)

    # Many-to-many relationship between Submission and Choice
    choices = models.ManyToManyField(Choice)

    def __str__(self):
        return f"Submission {self.id}"
