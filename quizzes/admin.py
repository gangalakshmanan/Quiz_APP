from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Quiz, Question, Choice, QuizTaker

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(QuizTaker)
