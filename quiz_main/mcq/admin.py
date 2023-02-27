from django.contrib import admin
from mcq.models import Quiz, Category, Question, Choice,regestration, Score
# Register your models here.
admin.site.register(Quiz)
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(regestration)
admin.site.register(Score)