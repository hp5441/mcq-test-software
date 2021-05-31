from django.urls import path
from . import views

urlpatterns = [
    path('<int:user>/', views.quiz_page),
    path('<int:user>/<int:quiz>/', views.quiz_specific_page),
    path('get-questions/', views.get_quiz_questions),
    path('submit-answer/', views.submit_quiz_response),
    path('create-quiz/', views.create_quiz),
    path('get-result/', views.get_result),
]
