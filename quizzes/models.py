from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
# from .models import Quiz

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=500)
    timer_seconds = models.IntegerField(default=60)  # Timer per question
    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    def __str__(self):
        return self.text

class QuizTaker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)
    is_validated = models.BooleanField(default=False)  # New field for validation
    validated_score = models.IntegerField(null=True, blank=True)  # Optional manual score

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"
  
