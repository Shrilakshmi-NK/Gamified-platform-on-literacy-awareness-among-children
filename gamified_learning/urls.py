from django.urls import path
from django.contrib.auth import views as auth_views  # Import Django's built-in password reset views
from . import views  # Import your views

urlpatterns = [
    # path('', views.home_view, name='home'),
    path('', views.login_user, name='login'),  # This will load the login page when the root URL is accessed
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('forgot-password/', auth_views.PasswordResetView.as_view(), name='forgot-password'),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('guest-login/', views.guest_login, name='guest-login'),
    path('dashboard/', views.dashboard, name='dashboard'),  # This line defines the 'dashboard' URL pattern
    path('stories/', views.stories, name='stories'),
    path('quiz/<int:story_id>/', views.quiz, name='quiz'),
    path('quiz-results/<int:story_id>/', views.quiz_results, name='quiz_results'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('feedback/', views.feedback, name='feedback'),
]




# from django.urls import path
# from django.contrib.auth import views as auth_views  # Import Django's built-in password reset views
# from . import views  # Import your views

# urlpatterns = [
#     path('login/', views.login_user, name='login'),
#     path('register/', views.register_user, name='register'),
#     path('forgot-password/', auth_views.PasswordResetView.as_view(), name='forgot-password'),
#     path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
#     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#     path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
#     path('guest-login/', views.guest_login, name='guest-login'),
# ]




# from django.urls import path
# from django.contrib.auth import views as auth_views  # Import Django's built-in password reset views
# from . import views

# urlpatterns = [
#     path('register/', views.register_user, name='register'),
#     path('guest-login/', views.guest_login, name='guest_login'),
#     path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard view
#     path('quiz/', views.quiz, name='quiz'),  # Quiz view
#     path('leaderboard/', views.leaderboard, name='leaderboard'),  # Leaderboard view
#     path('submit-feedback/', views.submit_feedback, name='submit_feedback'),  # Feedback view
#     path('stories/', views.stories, name='stories'),  # Stories view
# ]
