from django.urls import path
from . import views

urlpatterns = [
    path('', views.sign_in),
    path('sign-up/', views.sign_up),
    path('teacher-sign-up/', views.teacher_sign_up),
    path('teacher-sign-in/', views.teacher_sign_in),
    path('student-sign-up/', views.student_sign_up),
    path('student-sign-in/', views.student_sign_in),
]
