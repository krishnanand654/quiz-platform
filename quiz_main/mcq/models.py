from django.db import models
from django.contrib.auth.models import User
import datetime


class regestration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    User_Name = models.CharField(max_length=50, null=False)
    Email = models.EmailField(unique=True, null=False)
    Password = models.CharField(max_length=100)
    def __str__(self):
        return self.User_Name


class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
class Quiz(models.Model):
    STATUS_CHOICES = (
        ('hard', 'Hard'),
        ('medium', 'Medium'),
        ('easy', 'Easy'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    difficulty_level = models.CharField(choices=STATUS_CHOICES,max_length=10, default='pending')

    created_date = models.DateField(
        auto_now=False, auto_now_add=True, editable=True)
    passing_score = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
        
    

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    
    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text

class Score(models.Model):
  
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)