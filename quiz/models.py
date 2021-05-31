from django.db import models
from user.models import School
from django.conf import settings


class Quiz(models.Model):
    """quiz model"""

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    pass_percentage = models.IntegerField(default=50)
    completed = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name


class QuizQuestion(models.Model):
    """question model contains the question statement"""

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    statement = models.TextField()

    def __str__(self) -> str:
        return self.statement


class QuizAnswer(models.Model):
    """answer model"""

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.answer


class QuizAttemptStatus(models.Model):
    """attempt model keeps track of a specific user's attempt at a specific quiz"""

    choices = [('C', 'completed'), ('I', 'incomplete'), ('N', 'notStarted')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=choices, default='N')
    current_index = models.IntegerField(default=0)
    time_taken = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.status

    def save(self, *args, **kwargs):
        super(QuizAttemptStatus, self).save(*args, **kwargs)
        if self.status == "C":
            try:
                self.quiz.completed += 1
                self.quiz.save()
            except:
                raise Exception("unable to increment quiz completed")


class AnswerStatus(models.Model):
    """answer status model keeps track of a specific user's submissions"""

    attempt = models.ForeignKey(QuizAttemptStatus, on_delete=models.CASCADE)
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    answer = models.ForeignKey(QuizAnswer, on_delete=models.CASCADE)
    correctness = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.answer.answer
