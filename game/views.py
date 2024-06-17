from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.contrib.auth import login,logout,authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from game.models import*
from .forms import*
import logging
logger = logging.getLogger('django')







#Index is working perfect
def index(request):
    categories = Category.objects.all()
    total_quiz_user = QuizUser.objects.order_by('-total_score')[:10]
    difficulties = Difficulty.objects.all()
    context = {'total_quiz_user':total_quiz_user,'categories': categories,'difficulties':difficulties,}
    return render(request,'html/index.html', context)


#Player login Route View
def quiz_login(request):
    title = 'Iniciar Sessão'
    form =  QuizUserLogin(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
        return redirect('quizz:quiz_user_home')
    context = {'title':title,'form':form}
    return render(request,'html/login.html',context)
        

#Player Logout Route view
def quiz_logout(request):
    logout(request)
    return redirect('quizz:index')


#user create account Route View
def quiz_user_register(request):
    title = 'Criar Conta de Competidor '
    if request.method == 'POST':
        form = QuizUserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quizz:quiz_login')
    else:
        form = QuizUserRegisterForm()
    context = {'form':form,'title':title}
    return render(request,'html/quiz_user.html',context)


def quizz_view_category(request, category_id=None):
    categories = Category.objects.all()
    category = get_object_or_404(Category, pk=category_id)
    comcept = get_object_or_404(Settings,category_id=category_id)
    difficulties = Difficulty.objects.all()
    return render(request, 'html/category.html', {'category': category,'categories': categories,'difficulties':difficulties,'comcept':comcept})


#Player Playing
@login_required
def quiz_play(request, category_id=None, difficulty_id=None):
    categories = Category.objects.all()
    difficulties = Difficulty.objects.all()
    quiz_user, created = QuizUser.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        answer_id = request.POST.get('answer_id')
        question_answered = quiz_user.choices.select_related('question').get(question_id=question_id)

       
        difficulty = request.POST.get('difficulty_id')
        category = request.POST.get('category_id')

        printlogger = logging.getLogger('django')
        print('parametro 1 - Nivel: ',difficulty)
        print('parametro 1 - Categoria',category)
        logger.info('here goes your message',difficulty)

        try:
            selected_option = question_answered.question.questions_options.get(pk=answer_id)
        except ObjectDoesNotExist:
            Http404
        print('parametro 2 - Nivel: ',difficulty)
        print('parametro 2 - Categoria',category)
        quiz_user.validate_attempt(question_answered,selected_option)
        return redirect('quizz:quiz_result_questions',question_answered.pk)

    else:
        question = quiz_user.get_new_questions()
        #if question is not None:
           # quiz_user.create_attempts(question)
        context = {'question':question,'categories':categories,'difficulties':difficulties}
    return render(request,'html/quiz_play.html',context)


def quiz_result_questions(request,question_answered_pk=None):
    categories = Category.objects.all()
    difficulties = Difficulty.objects.all()
    answered = get_object_or_404(Result,pk=question_answered_pk)
    context = {'answered':answered,'categories':categories,'difficulties':difficulties }
    return render(request,'html/quiz_results.html',context)


#Rules
@login_required
def ranking(request):
    labels = []
    data = []
    categories = Category.objects.all()
    total_quiz_user = QuizUser.objects.order_by('-total_score')[:10]
    for quiz_user in total_quiz_user:
        labels.append(quiz_user.user.username) 
        data.append(int(quiz_user.total_score))
    user_counter = total_quiz_user.count()
    context = {'categories': categories,'user_counter':user_counter,'total_quiz_user':total_quiz_user,'labels':labels,'data':data}
    return render(request, 'html/ranking.html',context)



def learning(request, category_id):
    categories = Category.objects.all()
    single_category = get_object_or_404(Category,pk=category_id)
    settings_list = Settings.objects.filter(category_id=category_id).order_by('-pub_date')
    
    paginator = Paginator(settings_list,1)
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        settings = paginator.page(page)
    except (EmptyPage, InvalidPage):
        settings = paginator.page(paginator.num_pages)

    context = {'categories': categories, 'settings':settings,'single_category':single_category}
    return render(request, 'html/learning.html',context)


#Rankink
def rules(request):
    categories = Category.objects.all()
    rules = Config.objects.all()
    context = {'categories': categories,'rules':rules}
    return render(request, 'html/rules.html',context)



























#Player Home Route View
@login_required
def quiz_user_home(request):
    return render(request,'html/quiz_user_home.html',)

