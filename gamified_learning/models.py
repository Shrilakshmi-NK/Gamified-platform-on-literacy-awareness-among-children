# from django.db import models

# # Create your models here.
# from django.contrib.auth.models import AbstractUser

# class CustomUser(AbstractUser):
#     is_guest = models.BooleanField(default=False)

# class Badge(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     points = models.IntegerField()

# class QuizResult(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     score = models.IntegerField()
#     date = models.DateTimeField(auto_now_add=True)

# class Content(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     file = models.FileField(upload_to='educational_content/')

# class Feedback(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     feedback = models.TextField()
#     date = models.DateTimeField(auto_now_add=True)



######modifed code

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    is_guest = models.BooleanField(default=False)

    # Fix the reverse accessor clash by adding related_name for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='customuser_groups',  # This resolves the conflict for groups
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='customuser_user_permissions',  # This resolves the conflict for user_permissions
        blank=True
    )

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    points = models.IntegerField()


class Story(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='stories/', blank=True, null=True)  # Optional: For story-related images
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Quiz(models.Model):
    story = models.ForeignKey(Story, related_name='quizzes', on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    options = models.JSONField()  # Store options as a list
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return f"Quiz for {self.story.title}"

class QuizResult(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

class Content(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='educational_content/')

class Feedback(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    feedback = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
