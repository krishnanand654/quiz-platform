from django.urls import path
from .views import CreateQuizView, CreateQuizCategoryView, CreateQuizQuestionView, CreateQuizChoiceView,  QuizDetailView,  userCreate,CheckAnswerView, QuizScoreView,QuizFilterView,QuizAnalyticsView,UserProfileView,Users
from .views import UserUpdateDetail,UserDeleteView,Category
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [


    
    # Users should be able to sign up, log in, and log out. The authentication system should use JWT tokens. 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  



    # Users should be able to create quizzes. Each quiz should have a title and a set of questions with multiple choices. 
    path('create-quiz/<int:user_id>', CreateQuizView.as_view(), name='create-quiz'),
    path('create-category/', CreateQuizCategoryView.as_view(), name='create-category'),
    path('create-question/', CreateQuizQuestionView.as_view(), name='create-question'),
    path('create-choice/', CreateQuizChoiceView.as_view(), name='create-choice'),


    #detail about quiz
    path('quizzes/detail/<int:pk>/',  QuizDetailView.as_view(), name='list-qs'),
    

    # Users should be able to take quizzes. Each quiz should have a set of questions with multiple choices, and the user should be able to select their answer. After the user has completed the quiz, the system should display their score
    path('quiz/<int:quiz_id>/question/<int:question_id>/answer/<int:choice_id>/user/<int:user_id>/', CheckAnswerView.as_view(),name="check_answer"),

    # Users should be able to view their quiz results. The system should display the user's score for each quiz they have taken. 
    path('user/<int:user_id>/quiz/<int:quiz_id>/score/', QuizScoreView.as_view()),

    # The system should display a list of available quizzes that users can take. 
    # Users should be able to filter quizzes by topic, difficulty level, and date created. 
    path('quizzes/', QuizFilterView.as_view(), name='quiz-filter'),

    # The system should display analytics on each quiz, such as the average score, the number of times the quiz has been taken, and the percentage of users who have passed the quiz. 
    path('quizzes/analytics/<int:quiz_id>/', QuizAnalyticsView.as_view(), name='quiz_analytics'),

    # Users should be able to view their profile, which should display their username, email, and a list of quizzes they have created. 
    path('profile/<int:user_id>',UserProfileView.as_view(), name='user-profile'),


    #Admin users should be able to manage users, including creating, editing, and deleting user accounts
    path('user-register/', userCreate.as_view(), name='user-register'),
    path('user-update/<int:user_id>', UserUpdateDetail.as_view(), name='user-update'),
    path('user-delete/<int:user_id>', UserDeleteView.as_view(), name='user-delete'),

    
    # show all users
    path('users/',Users.as_view(), name='user-profile'),
    path('categories/',Category.as_view(), name='user-profile'),

]
