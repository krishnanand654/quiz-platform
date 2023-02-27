from rest_framework import generics,status
from rest_framework.response import Response
from .models import Category, Quiz, Question, Choice,regestration, User, Score
from .serializers import QuizCategorySerializer, QuizSerializer, QuizQuestionSerializer, QuizChoiceSerializer,ObtainTokenPairSerializer,QuizCreateSerializer
from .serializers import userSerializer,UserDetailSerializer,userTestSerializer,categorySerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.db.models import Avg, Count
from rest_framework.filters import BaseFilterBackend
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.views import TokenObtainPairView





class ObtainTokenPairView(TokenObtainPairView):
    serializer_class = ObtainTokenPairSerializer

    
class userCreate(generics.CreateAPIView):  # create user
    queryset = regestration.objects.all()
    serializer_class = userSerializer
   


class CreateQuizView(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = QuizCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.kwargs['user_id'])

class CreateQuizCategoryView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = QuizCategorySerializer


class CreateQuizQuestionView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Question.objects.all()
    serializer_class = QuizQuestionSerializer


class CreateQuizChoiceView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Choice.objects.all()
    serializer_class = QuizChoiceSerializer

# list quiz
class QuizDetailView(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def retrieve(self, request, *args, **kwargs):
        quiz = self.get_object()
        serializer = self.get_serializer(quiz)

        data = serializer.data
        data['questions'] = []

        questions = Question.objects.filter(quiz=quiz)

        for question in questions:
            question_data = QuizQuestionSerializer(question).data
            question_data['choices'] = QuizChoiceSerializer(Choice.objects.filter(question=question), many=True).data
            data['questions'].append(question_data)
        
        return Response(data)
      

class CheckAnswerView(generics.RetrieveAPIView):
   permission_classes = [IsAuthenticated]
   def get(self, request, quiz_id, user_id, question_id, choice_id):
        # get the quiz, question, and choice objects from the database
        try:
            quiz = get_object_or_404(Quiz, id=quiz_id)
            question = get_object_or_404(Question, id=question_id)
            choice = get_object_or_404(Choice, id=choice_id)

            # check if the choice is correct for the given question
            is_correct = False
            print(quiz)
            print(question)
            if choice.question == question and choice.is_correct:
                is_correct = True

            # update user's score if the answer is correct
            if is_correct:
                user = get_object_or_404(User, id=user_id)
                score, created = Score.objects.get_or_create(user=user, quiz=quiz)
                score.value += 1
                score.save()

            if is_correct:
                message = "Congratulations! Your answer is correct."
            
            else:
                message = "Sorry, your answer is incorrect."
            return Response({'message': message})
        except ObjectDoesNotExist:
            return Response({'error': 'Quiz matching query does not exist.'}, status=404)
        
        

class QuizScoreView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id, quiz_id):
        # get the quiz and user objects from the database
        quiz = get_object_or_404(Quiz, id=quiz_id)
        user = get_object_or_404(User, id=user_id)

        # retrieve the user's score for the given quiz
        score = get_object_or_404(Score, quiz=quiz, user=user)

        return Response({'quiz':quiz.name,'score': score.value})
 

class QuizFilterBackend(BaseFilterBackend):
    
    
    def filter_queryset(self, request, queryset, view):
        created_date = request.query_params.get('created_date', None)
        difficulty_level = request.query_params.get('difficulty_level', None)
        category_name = request.query_params.get('category_name', None)
        
        if created_date:
            queryset = queryset.filter(created_date=date.fromisoformat(created_date))
        if difficulty_level:
            queryset = queryset.filter(difficulty_level=difficulty_level)
        if category_name:
            queryset = queryset.filter(category__name=category_name)
        
        return queryset


class QuizFilterView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuizSerializer
    filter_backends = [QuizFilterBackend]
    queryset = Quiz.objects.all()


class QuizAnalyticsView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(id=quiz_id)
            scores = Score.objects.filter(quiz=quiz)
            total_num_attempts = scores.count()
            avg_score = scores.aggregate(Avg('value'))['value__avg']
            num_passed = scores.filter(value__gte=quiz.passing_score).count()
            pass_percentage = (num_passed / total_num_attempts) * 100 if total_num_attempts > 0 else 0

            analytics_data = {
                'quiz_id': quiz_id,
                'quiz_name': quiz.name,
                'total_num_attempts': total_num_attempts,
                'avg_score': avg_score,
                'num_passed': num_passed,
                'pass_percentage': pass_percentage
            }

            return Response(analytics_data)
        except ObjectDoesNotExist:
            return Response({'error': 'Quiz matching query does not exist.'}, status=404)
        


class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field='user_id'
    queryset = regestration.objects.all()
    serializer_class = UserDetailSerializer


class Users(generics.ListAPIView):
    queryset = regestration.objects.all()
    serializer_class = userTestSerializer

class UserUpdateDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    lookup_field = 'user_id'  # details of particular employee
    queryset = regestration.objects.all()
    serializer_class = userSerializer
    


class UserDeleteView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    lookup_field = 'user_id'
    queryset = regestration.objects.all()
    serializer_class = userSerializer
   


class Category(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = categorySerializer




   
# class QuizListView(generics.RetrieveAPIView):
   
#     permission_classes = [IsAuthenticated]
#     queryset = Quiz.objects.all()
#     def get(self, request):
#         user_id = request.user.id
#         quizzes = Quiz.objects.all()
#         serializer = QuizSerializer(quizzes, many=True)
#         return Response(serializer.data)