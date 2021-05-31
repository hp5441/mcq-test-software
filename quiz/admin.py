from django.contrib import admin
from quiz.models import Quiz, QuizQuestion, QuizAnswer, QuizAttemptStatus, AnswerStatus

admin.site.register([Quiz, QuizQuestion, QuizAnswer,
                     QuizAttemptStatus, AnswerStatus])
