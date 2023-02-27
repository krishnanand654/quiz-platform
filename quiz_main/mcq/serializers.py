# serializers.py
from rest_framework import serializers
from .models import Category, Quiz, Question, Choice,regestration
from django.contrib.auth.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer




class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = regestration
        fields = ('User_Name','Email','Password')
    
    def create(self, validated_data):
        username = validated_data.get('User_Name')
        email = validated_data.get('Email')
        password = validated_data.get('Password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(username, email, password)

        validated_data['user'] = user
        user_reg = regestration.objects.create(**validated_data)
        return user_reg

class QuizCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class QuizCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['name','difficulty_level','category','passing_score']


class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model =Question
        fields = '__all__'


class QuizChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'


class QuizSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id','user_id','name', 'category_name','difficulty_level','created_date']

    def get_category_name(self, obj):
        return obj.category.name


class ObtainTokenPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email

        return token


class QuizProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields= ['name']


class UserDetailSerializer(serializers.ModelSerializer):
    quizzes = serializers.SerializerMethodField()

    class Meta:
        model = regestration
        fields = ['User_Name', 'Email', 'quizzes']

    def get_quizzes(self, obj):
        queryset = Quiz.objects.filter(user=obj.user)
        serializer = QuizProfileSerializer(queryset, many=True)
        return serializer.data
    

class userTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = regestration
        fields = '__all__'

    

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'






