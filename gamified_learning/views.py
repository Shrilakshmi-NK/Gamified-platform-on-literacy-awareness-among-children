from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .models import CustomUser, Badge, Content, QuizResult, Feedback, Story, Quiz
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
# from django.contrib.auth.decorators import login_required

def home_view(request):
    return render(request, 'gamified_learning/home.html')


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'gamified_learning/register.html', {'form': form})


def guest_login(request):
    guest_user, created = CustomUser.objects.get_or_create(
        username='Guest',
        defaults={'is_guest': True}
    )
    login(request, guest_user)
    return redirect('dashboard')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'gamified_learning/login.html', {'error': 'Invalid credentials'})
    return render(request, 'gamified_learning/login.html')


def dashboard(request):
    badges = Badge.objects.all()
    content = Content.objects.all()
    stories = Story.objects.all().order_by('-created_at')[:3]
    return render(request, 'gamified_learning/dashboard.html', {'badges': badges, 'content': content, 'stories': stories})


def quiz(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    quizzes = Quiz.objects.filter(story=story)
    if request.method == 'POST':
        score = calculate_score(request.POST, quizzes)
        QuizResult.objects.create(user=request.user, score=score, story=story)
        return redirect('dashboard')
    return render(request, 'gamified_learning/quiz.html', {'story': story, 'quizzes': quizzes})


def calculate_score(quiz_data, quizzes):
    score = 0
    for quiz in quizzes:
        user_answer = quiz_data.get(f"answer_{quiz.id}")
        if user_answer == quiz.correct_answer:
            score += 1
    return score


def quiz_results(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    results = QuizResult.objects.filter(story=story).order_by('-score')
    return render(request, 'gamified_learning/quiz_results.html', {'story': story, 'results': results})


def leaderboard(request):
    results = QuizResult.objects.order_by('-score')[:10]
    return render(request, 'gamified_learning/leaderboard.html', {'results': results})


# def feedback(request):
#     if request.method == 'POST':
#         Feedback.objects.create(user=request.user, feedback=request.POST['feedback'])
#         return redirect('dashboard')
#     return render(request, 'gamified_learning/feedback.html')

def feedback(request):
    if request.method == 'POST':
        # Fetch the 'comments' field from the POST data
        comments = request.POST.get('comments', '')

        # Ensure comments are not empty
        if not comments.strip():
            return HttpResponse("Feedback cannot be empty.", status=400)

        # Create feedback entry
        if request.user.is_authenticated:
            Feedback.objects.create(user=request.user, feedback=comments)
            return redirect('dashboard')
        else:
            return HttpResponse("User not authenticated.", status=403)

    return render(request, 'gamified_learning/feedback.html')

# @login_required
# def feedback(request):
#     if request.method == 'POST':
#         # Fetch the 'comments' field from the POST data
#         comments = request.POST.get('comments', '')

#         # Ensure comments are not empty
#         if not comments.strip():
#             return HttpResponse("Feedback cannot be empty.", status=400)

#         # Create feedback entry
#         Feedback.objects.create(user=request.user, feedback=comments)
#         return redirect('dashboard')

#     return render(request, 'gamified_learning/feedback.html')

def stories(request):
    stories = Story.objects.all().order_by('-created_at')
    return render(request, 'gamified_learning/stories.html', {'stories': stories})



# from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate
# from django.shortcuts import get_object_or_404
# from .models import CustomUser, Badge, Content, QuizResult, Feedback, Story, Quiz
# from django.contrib.auth.forms import UserCreationForm


# def home_view(request):
#     return render(request, 'gamified_learning/home.html') 

# # User registration view
# def register_user(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('dashboard')
#     else:
#         form = UserCreationForm()
#     return render(request, 'gamified_learning/register.html', {'form': form})

# # Guest login view
# # def guest_login(request):
# #     guest_user = CustomUser.objects.filter(username='Guest').first()
# #     if not request.user.is_authenticated:
# #          guest_user = CustomUser.objects.create(username='Guest', is_guest=True)
# #          login(request, guest_user)
# #     request.session['guest_user_id'] = guest_user.id
# #     return redirect('dashboard')

#   # Assuming you have a CustomUser model

# def guest_login(request):
#     # Check if a guest user already exists
#     guest_user, created = CustomUser.objects.get_or_create(
#         username='Guest', 
#         defaults={'is_guest': True}  # Default values for fields
#     )

#     # If needed, you can handle further logic for whether the user was newly created or existing
#     if created:
#         print("New guest user created.")
#     else:
#         print("Existing guest user fetched.")

#     # Proceed with the login process, e.g., setting session, redirecting
#     request.session['guest_user_id'] = guest_user.id
#     return redirect('dashboard')

# # Login view
# def login_user(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('dashboard')  # Redirect to a homepage or another page after login
#         else:
#             return render(request, 'gamified_learning/login.html', {'error': 'Invalid credentials'})
#     return render(request, 'gamified_learning/login.html')

# # Dashboard view
# def dashboard(request):
#     badges = Badge.objects.all()
#     content = Content.objects.all()
#     stories = Story.objects.all().order_by('-created_at')[:3]  # Show the latest 3 stories
#     return render(request, 'gamified_learning/dashboard.html', {'badges': badges, 'content': content})

# Quiz view
# def quiz(request, story_id):
#     if request.method == 'POST':
#         score = calculate_score(request.POST)  # Calculate quiz score
#         QuizResult.objects.create(user=request.user, score=score)
#         return redirect('dashboard')
#     return render(request, 'gamified_learning/quiz.html')

# def quiz(request, story_id):
#     # Get the specific story using the passed story_id
#     story = get_object_or_404(Story, id=story_id)
#     if request.method == 'POST':
#         # Calculate the score based on the quiz submission
#         score = calculate_score(request.POST)       
#         # Save the quiz result with the user's score
#         QuizResult.objects.create(user=request.user, score=score, story=story)      
#         # Redirect to the dashboard after submitting the quiz
#         return redirect('dashboard')
#     # Render the quiz page and pass the story data to the template
#     return render(request, 'gamified_learning/quiz.html', {'story': story})

# # Function to calculate quiz score
# def calculate_score(quiz_data):
#     score = 0
#     # Assuming quiz_data contains answers for each question, adjust as needed
#     for question, answer in quiz_data.items():
#         correct_answer = get_correct_answer(question)  # Implement this function to get the correct answer
#         if answer == correct_answer:
#             score += 1
#     return score

# # Function to get the correct answer for a question (you need to define the logic)
# def get_correct_answer(question):
#     # Example implementation (this should be replaced with your own logic)
#     correct_answers = {
#         'question1': 'answer1',
#         'question2': 'answer2',
#         # Add other questions and answers
#     }
#     return correct_answers.get(question, '')


#updated quiz forms
# def quiz(request, story_id):
#     # Get the specific story using the passed story_id
#     story = get_object_or_404(Story, id=story_id)
    
#     # Get all quizzes related to the story
#     quizzes = Quiz.objects.filter(story=story)

#     if request.method == 'POST':
#         # Calculate the score based on the quiz submission
#         score = calculate_score(request.POST, quizzes)
        
#         # Save the quiz result with the user's score
#         QuizResult.objects.create(user=request.user, score=score, story=story)
        
#         # Redirect to the dashboard after submitting the quiz
#         return redirect('dashboard')
    
#     # Render the quiz page and pass the story and quiz data to the template
#     return render(request, 'gamified_learning/quiz.html', {'story': story, 'quizzes': quizzes})

# # Function to calculate quiz score
# def calculate_score(quiz_data, quizzes):
#     score = 0
#     # Loop through each quiz and check if the answer matches the correct answer
#     for quiz in quizzes:
#         # Retrieve the user's answer for the question
#         user_answer = quiz_data.get(f"answer_{quiz.id}")
#         if user_answer == quiz.correct_answer:
#             score += 1
#     return score
# 
# def quiz(request, story_id):
#     # Get the specific story using the passed story_id
#     story = get_object_or_404(Story, id=story_id)
    
#     # Get all quizzes related to the story
#     quizzes = Quiz.objects.filter(story=story)

#     if request.method == 'POST':
#         # Calculate the score based on the quiz submission
#         score = calculate_score(request.POST, quizzes)
        
#         # Save the quiz result with the user's score
#         QuizResult.objects.create(user=request.user, score=score)
        
#         # Redirect to the dashboard after submitting the quiz
#         return redirect('dashboard')
    
#     # Render the quiz page and pass the story and quiz data to the template
#     return render(request, 'gamified_learning/quiz.html', {'story': story, 'quizzes': quizzes})


# # Function to calculate quiz score
# def calculate_score(quiz_data, quizzes):
#     score = 0
#     # Loop through each quiz and check if the answer matches the correct answer
#     for quiz in quizzes:
#         # Retrieve the user's answer for the question
#         user_answer = quiz_data.get(f"answer_{quiz.id}")
#         if user_answer == quiz.correct_answer:
#             score += 1
#     return score

# # Leaderboard view
# def leaderboard(request):
#     results = QuizResult.objects.order_by('-score')[:10]
#     return render(request, 'gamified_learning/leaderboard.html', {'results': results})

# # Feedback submission view
# def feedback(request):
#     if request.method == 'POST':
#         feedback = request.POST['feedback']
#         Feedback.objects.create(user=request.user, feedback=feedback)
#         return redirect('dashboard')
#     return render(request, 'gamified_learning/feedback.html')

# # View to display stories
# def stories(request):
#     stories = Story.objects.all().order_by('-created_at')  # Fetch all stories, ordered by newest first
#     return render(request, 'gamified_learning/stories.html', {'stories': stories})





# # from django.shortcuts import render

# # # Create your views here.


# # from django.shortcuts import render, redirect
# # from django.contrib.auth import login, authenticate
# # from .models import CustomUser
# # from django.contrib.auth.forms import UserCreationForm
# # from .models import Badge, Content, QuizResult
# # def register_user(request):
# #     if request.method == 'POST':
# #         form = UserCreationForm(request.POST)
# #         if form.is_valid():
# #             user = form.save()
# #             login(request, user)
# #             return redirect('dashboard')
# #     else:
# #         form = UserCreationForm()
# #     return render(request, 'register.html', {'form': form})

# # def guest_login(request):
# #     guest_user = CustomUser.objects.create(username='Guest', is_guest=True)
# #     login(request, guest_user)
# #     return redirect('dashboard')

# # def dashboard(request):
# #     badges = Badge.objects.all()
# #     content = Content.objects.all()
# #     return render(request, 'dashboard.html', {'badges': badges, 'content': content})

# # def quiz(request):
# #     if request.method == 'POST':
# #         # Process quiz results
# #         score = calculate_score(request.POST)  # Implement this function
# #         QuizResult.objects.create(user=request.user, score=score)
# #         return redirect('dashboard')
# #     return render(request, 'quiz.html')

# # def leaderboard(request):
# #     results = QuizResult.objects.order_by('-score')[:10]
# #     return render(request, 'leaderboard.html', {'results': results})

# # def submit_feedback(request):
# #     if request.method == 'POST':
# #         feedback = request.POST['feedback']
# #         Feedback.objects.create(user=request.user, feedback=feedback)
# #         return redirect('dashboard')
# #     return render(request, 'feedback.html')


# #####updated code

# from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate
# from .models import CustomUser, Badge, Content, QuizResult, Feedback, Story
# from django.contrib.auth.forms import UserCreationForm

# # Function to calculate quiz score
# def calculate_score(quiz_data):
#     score = 0
#     # Assuming quiz_data contains answers for each question, adjust as needed
#     for question, answer in quiz_data.items():
#         correct_answer = get_correct_answer(question)  # Implement this function to get the correct answer
#         if answer == correct_answer:
#             score += 1
#     return score

# # Function to get the correct answer for a question (you need to define the logic)
# def get_correct_answer(question):
#     # Example implementation (this should be replaced with your own logic)
#     # You can store correct answers in your database and query them
#     correct_answers = {
#         'question1': 'answer1',
#         'question2': 'answer2',
#         # Add other questions and answers
#     }
#     return correct_answers.get(question, '')

# # User registration view
# def register_user(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('dashboard')
#     else:
#         form = UserCreationForm()
#     return render(request, 'gamified_learning/register.html', {'form': form})

# # Guest login view
# def guest_login(request):
#     guest_user = CustomUser.objects.create(username='Guest', is_guest=True)
#     login(request, guest_user)
#     return redirect('dashboard')

# # Dashboard view
# def dashboard(request):
#     badges = Badge.objects.all()
#     content = Content.objects.all()
#     stories = Story.objects.all().order_by('-created_at')[:3]  # Show the latest 3 stories
#     return render(request, 'gamified_learning/dashboard.html', {'badges': badges, 'content': content})

# # Quiz view
# def quiz(request):
#     if request.method == 'POST':
#         score = calculate_score(request.POST)  # Calculate quiz score
#         QuizResult.objects.create(user=request.user, score=score)
#         return redirect('dashboard')
#     return render(request, 'gamified_learning/quiz.html')

# # Leaderboard view
# def leaderboard(request):
#     results = QuizResult.objects.order_by('-score')[:10]
#     return render(request, 'gamified_learning/leaderboard.html', {'results': results})

# # Feedback submission view
# def submit_feedback(request):
#     if request.method == 'POST':
#         feedback = request.POST['feedback']
#         Feedback.objects.create(user=request.user, feedback=feedback)
#         return redirect('dashboard')
#     return render(request, 'gamified_learning/feedback.html')

# # View to display stories
# def stories(request):
#     stories = Story.objects.all().order_by('-created_at')  # Fetch all stories, ordered by newest first
#     return render(request, 'gamified_learning/stories.html', {'stories': stories})