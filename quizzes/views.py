from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Choice, QuizTaker
from .forms import RegisterForm, QuizForm
from django.contrib import messages

def student_list(request):
    return render(request, 'student_list.html', {'message': 'Student List Page (Under Construction)'})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quiz_list')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.POST.get('next', request.GET.get('next', '/'))  # Default to quiz list
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             return redirect('quiz_list')
#         else:
#             messages.error(request, 'Invalid credentials')
#     return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

@login_required
def take_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.questions.all()
    if request.method == 'POST':
        form = QuizForm(request.POST, questions=questions)
        if form.is_valid():
            score = 0
            for question in questions:
                choice_id = form.cleaned_data[f'question_{question.id}']
                choice = Choice.objects.get(id=choice_id)
                if choice.is_correct:
                    score += 1
            QuizTaker.objects.create(user=request.user, quiz=quiz, score=score, is_validated=False)
            messages.success(request, "Quiz submitted for validation.")
            return redirect('result_pending', quiz_id=quiz.id)
    else:
        form = QuizForm(questions=questions)
    return render(request, 'take_quiz.html', {'quiz': quiz, 'form': form})

@login_required
# from .models import QuizTaker

def result_pending(request, quiz_id):
    pending_results = QuizTaker.objects.filter(
        quiz_id=quiz_id, 
        is_validated=False
    ).order_by('-completed_at')  # ✅ Use valid field

    return render(request, 'result_pending.html', {'pending_results': pending_results})

# def result_pending(request, quiz_id):
#     quiz = Quiz.objects.get(id=quiz_id)
#     submission = QuizTaker.objects.filter(user=request.user, quiz=quiz).latest('submitted_at')
#     return render(request, 'result_pending.html', {'quiz': quiz, 'submission': submission})
@login_required
def result(request, quiz_id):
    quiz_taker = QuizTaker.objects.get(user=request.user, quiz_id=quiz_id)
    return render(request, 'result.html', {'quiz_taker': quiz_taker})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def questions_page(request):
    return render(request, 'questions.html')
@login_required
def quiz_keywords_page(request):
    return render(request, 'quiz_keywords.html')

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from .models import QuizTaker

@staff_member_required
def validate_quiz(request):
    submissions = QuizTaker.objects.filter(is_validated=False).order_by('submitted_at')
    if request.method == 'POST':
        submission_id = request.POST.get('submission_id')
        new_score = request.POST.get('validated_score')
        if submission_id and new_score:
            submission = QuizTaker.objects.get(id=submission_id)
            submission.validated_score = int(new_score)
            submission.is_validated = True
            submission.save()
            return redirect('validate_quiz')
    return render(request, 'admin_validate_quiz.html', {'submissions': submissions})