from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'quizz'
urlpatterns = [
    path('', views.index, name='index'),
    #path('<int:category_id>/', views.list_of_levels, name='list_of_levels'),
    #path('<int:category_id>/<int:level_id>/', views.list_of_questions, name='list_of_questions'),
    path('<int:category_id>/', views.quizz_view, name='quizz_view'),
    #path('<int:category_id>/', views.playing, name='playing'),
    path('rules/', views.rules, name='rules'),
    path('ranking/', views.ranking, name='ranking'),

    path('login/', views.quiz_login, name='quiz_login'),
    path('logout/',views.quiz_logout, name='quiz_logout'),
    path('create/a/count', views.quiz_user_register, name='quiz_user_register'),


    path('user/home/', views.quiz_user_home, name='quiz_user_home'),
    path('quiz/play/', views.quiz_play, name='quiz_play'),
    path('result/<int:question_answered_pk>/', views.quiz_result_questions, name='quiz_result_questions'),
    
]




    