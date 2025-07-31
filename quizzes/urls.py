from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('result/<int:quiz_id>/', views.result, name='result'),
    path('students/', views.student_list, name='student_list'),
    path('questions/', views.questions_page, name='questions_page'),
    path('quiz-keywords/', views.quiz_keywords_page, name='quiz_keywords_page'),
    path('admin/validate-quiz/', views.validate_quiz, name='validate_quiz'),
    path('result/pending/<int:quiz_id>/', views.result_pending, name='result_pending'),
]