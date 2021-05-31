from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_view),
    path('logout/', views.logout_view),
    path('signin/', views.sign_in),
    path('signin/sign-up/', views.sign_up),
    path('signin/teacher-sign-up/', views.teacher_sign_up),
    path('signin/teacher-sign-in/', views.teacher_sign_in),
    path('signin/student-sign-up/', views.student_sign_up),
    path('signin/student-sign-in/', views.student_sign_in),
]
