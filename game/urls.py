from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'quizz'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/a/count', views.quiz_user_register, name='quiz_user_register'),
    path('login/', views.quiz_login, name='quiz_login'),
    path('logout/',views.quiz_logout, name='quiz_logout'),
    path('rules/', views.rules, name='rules'),
    path('ranking/', views.ranking, name='ranking'),
    path('<int:category_id>/', views.quizz_view_category, name='quizz_view_category'),
    path('<int:category_id>/learning/', views.learning, name='learning'),
    path('<int:category_id>/<int:difficulty_id>/play/', views.quiz_play, name='quiz_play'),
    path('user/home/', views.quiz_user_home, name='quiz_user_home'),
    path('result/<int:question_answered_pk>/', views.quiz_result_questions, name='quiz_result_questions'),
]




    