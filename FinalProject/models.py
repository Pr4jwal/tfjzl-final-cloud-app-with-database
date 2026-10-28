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
    # Establishing a many-to-many relationship as a question can belong to one or more lessons and a lesson can have many questions
    lessons =  models.ManyToManyField(Lesson)
    question_text = models.CharField(max_length=500)
    question_point = models.IntegerField(default=1)

    def is_get_grade(self, selected_ids):
        """ this function checks if the student successfully chose all the right answers """
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        if all_answers == selected_correct:
            return True
        else:
            return False

class Choice(models.Model):
    # Has a one-to-many relationship with Question model
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

class Submission(models.Model):
   # One enrollment can have multiple submissions
   enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
   # A submission can have multiple choices and a choice can belong to multiple submissions
   choices = models.ManyToManyField(Choice)
