from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'detlog'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:category_id>/', views.list_of_levels, name='list_of_levels'),
    #path('<int:category_id>/<int:level_id>/', views.list_of_questions, name='list_of_questions'),
    path('<int:category_id>/<int:level_id>/', views.list_of_questions, name='list_of_questions'),
    path('<int:category_id>/<int:level_id>/', views.playing, name='playing'),
    path('rules/', views.rules, name='rules'),
    path('ranking/', views.ranking, name='ranking'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


    path('<int:question_id>/submit/', views.submit, name='submit'),
    path('scores/', views.scores, name='scores'),
    
]




    