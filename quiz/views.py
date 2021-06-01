from django.http.response import JsonResponse
from quiz.models import QuizAnswer, QuizQuestion, Quiz, QuizAttemptStatus, AnswerStatus
from django.shortcuts import redirect, render
from .utils import get_json


def quiz_page(request, user):
    """quiz page shows a list of quizzes accessible to that particular student's school"""

    if(user == request.user.pk and not request.user.is_teacher):
        quizs = Quiz.objects.filter(school=request.user.school)
        context = {'quizs': quizs}
        return render(request, 'quiz_pages/quiz_page.html', context)
    return redirect("/")


def quiz_specific_page(request, user, quiz):
    """quiz specific page view shows the quiz with mcq options"""

    if(user == request.user.pk and not request.user.is_teacher):
        quiz_object = Quiz.objects.filter(pk=int(quiz))
        if len(quiz_object) and request.user.school.pk == quiz_object.school.pk:
            quiz_status, created = QuizAttemptStatus.objects.get_or_create(user=request.user,
                                                                           quiz=Quiz.objects.get(pk=quiz))
            context = {"status": quiz_status}
            return render(request, 'quiz_pages/quiz_specific_page.html', context)
    return redirect("/")


def get_quiz_questions(request):
    """AJAX request which serves a JSON containing a list of questions and its possible answers"""

    if request.method == "POST" and not request.user.is_teacher:

        quiz = request.POST.get("quiz")

        if request.user.school.pk == Quiz.objects.get(pk=int(quiz)).school.pk:
            questions = list(QuizQuestion.objects.filter(
                quiz=Quiz.objects.get(pk=int(quiz))).order_by('pk').values('pk', 'statement'))

            answers = list(QuizAnswer.objects.filter(
                quiz=Quiz.objects.get(pk=int(quiz))).order_by('question__pk').values('question', 'answer', 'pk'))
            data = {"answers": answers, "questions": questions}
            return JsonResponse(data, safe=False)
    return redirect("/")


def submit_quiz_response(request):
    """AJAX request which records the user's response and returns a JSON of the correct answer"""

    if request.method == "POST" and not request.user.is_teacher:
        print(request.POST)
        quiz = request.POST.get("quiz")
        if request.user.school.pk == Quiz.objects.get(pk=int(quiz)).school.pk:
            question = request.POST.get("question")
            answers = request.POST.getlist("answers[]")
            index = request.POST.get("index")
            time = request.POST.get("time")
            correctness = True
            print(answers, index)
            try:
                actual_answers = list(QuizAnswer.objects.filter(
                    question=QuizQuestion.objects.get(
                        pk=question), is_correct=True).order_by('pk').values("pk", "answer"))

                if(len(actual_answers) != len(answers)):
                    correctness = False
                else:
                    for_check = set(map(int, answers))
                    for correct_ans in actual_answers:
                        if correct_ans.get("pk") not in for_check:
                            correctness = False

                attempt_status = QuizAttemptStatus.objects.get(
                    user=request.user, quiz=Quiz.objects.get(pk=int(quiz)))

                for ans in answers:
                    print(ans)
                    AnswerStatus.objects.create(attempt=attempt_status, question=QuizQuestion.objects.get(
                        pk=question), answer=QuizAnswer.objects.get(pk=int(ans)), correctness=correctness)

            except:
                raise Exception(
                    "error in updating answer or quiz attempt statuses")
            else:
                if int(index) == 10:
                    attempt_status.status = "C"
                else:
                    attempt_status.status = "I"
                attempt_status.current_index = index
                attempt_status.time_taken = time
                attempt_status.save()
            return JsonResponse({"actual-answers": actual_answers, "quiz-status": attempt_status.status}, safe=False)
    return redirect("/")


def get_result(request):
    """AJAX request which serves details of the user's quiz attempt details in JSON"""

    if request.method == "POST" and not request.user.is_teacher:
        quiz = request.POST.get("quiz")
        if request.user.school.pk == Quiz.objects.get(pk=int(quiz)).school.pk:
            quiz_object = Quiz.objects.get(pk=int(quiz))
            attempt = QuizAttemptStatus.objects.get(
                user=request.user, quiz=quiz_object)
            answers = list(AnswerStatus.objects.filter(attempt=attempt).distinct(
                "question").values("question", "correctness"))
            time = attempt.time_taken
            return JsonResponse({"attempt-data": answers, "time-taken": time}, safe=False)
        else:
            return JsonResponse({"error": "user not authorised"}, safe=False)
    return redirect("/")


def create_quiz(request):
    """AJAX request accessible to teachers to create quizzes for their particular school (uses opentdb)"""

    if request.method == "POST" and request.user.is_teacher:
        quiz = None
        """uses utility function to get random questions from opentdb"""
        data = get_json()

        try:
            quiz = Quiz.objects.create(name=request.POST.get(
                'quizname'), type='single', school=request.user.school, pass_percentage=request.POST.get('percent'))
        except:
            raise Exception("error in creating quiz")

        for record in data:
            question = record.get('question')
            try:
                quiz_question = QuizQuestion.objects.create(
                    quiz=quiz, statement=question)
                QuizAnswer.objects.create(quiz=quiz, question=quiz_question, answer=record.get(
                    'correct_answer'), is_correct=True)
                for answer in record.get('incorrect_answers'):
                    QuizAnswer.objects.create(
                        quiz=quiz, question=quiz_question, answer=answer)
            except:
                quiz.delete()
                raise Exception("error while creating questions and answers")
        return redirect("/quiz/create-quiz/")

    active_quizs = Quiz.objects.filter(school=request.user.school)
    context = {'quizes': active_quizs}

    return render(request, 'quiz_pages/create_quiz.html', context)


def delete_quiz(request):
    """AJAX request accessible to teachers to delete quizzes"""

    if(request.method == "POST" and request.user.is_teacher):
        quiz = request.POST.get("quiz_pk")
        try:
            Quiz.objects.get(pk=int(quiz)).delete()
        except:
            raise Exception("unable to delete quiz")
    return redirect("/")
