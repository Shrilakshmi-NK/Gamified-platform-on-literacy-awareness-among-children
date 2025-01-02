from django.contrib import admin

# Register your models here.
from .models import Story, Badge, Content, QuizResult, Feedback, Quiz

# Register your models here
admin.site.register(Story)
admin.site.register(Badge)
admin.site.register(Content)
admin.site.register(Quiz)
admin.site.register(QuizResult)
admin.site.register(Feedback)
