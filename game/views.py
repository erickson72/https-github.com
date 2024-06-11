from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import time
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from .models import*
from .forms import*
from django.forms import formset_factory
from django.contrib.auth import views as auth_views
import logging




#Index is working perfect
def index(request):
    categories = Category.objects.all()
    return render(request,'html/index.html', {'categories': categories})

##List of levels are working perfect
def list_of_levels(request, category_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, pk=category_id)
    levels = Level.objects.all()
    return render(request, 'html/category.html', {'category': category, 'levels': levels,'categories': categories})

#List of questions are working perfect
def list_of_questions(request, category_id,level_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, pk=category_id)
    level = get_object_or_404(Level, pk=level_id)
    questions = Question.objects.filter(category=category,level=level).order_by('category').order_by('level')

    paginator = Paginator(questions,1)
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        questions_in_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        questions_in_page = paginator.page(paginator.num_pages)

    for q in questions_in_page:
        question = get_object_or_404(Question, pk=q.pk)
        if not question:
             return render(request,'html/no_questions.html',{'category':category,'level': level, 'questions': questions_in_page,'categories': categories,})
        context = {'category':category,'level': level, 'questions': questions_in_page,'categories': categories,'question':question}
    if not questions_in_page:
        return render(request, 'html/no_questions.html',{'category':category,'level': level, 'questions': questions_in_page,'categories': categories,})
    return render(request, 'html/questions.html', context)



#Jogar
def quiz(request,category_id,level_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, pk=category_id)
    level = get_object_or_404(Level, pk=level_id)
    questions = Question.objects.filter(category=category,level=level).order_by('category').order_by('level')
    
    paginator = Paginator(questions,1)
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        questions_in_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        questions_in_page = paginator.page(paginator.num_pages)

    for q in questions_in_page:
        question = get_object_or_404(Question, pk=q.pk)
        if not question:
             return render(request,'html/no_questions.html',{'category':category,'level': level, 'questions': questions_in_page,'categories': categories})
        context = {'category':category,'level': level, 'questions': questions_in_page,'categories': categories,'question':question}
    if not questions_in_page:
        return render(request, 'html/no_questions.html',{'category':category,'level': level, 'questions': questions_in_page,'categories': categories})
    return render(request, 'html/questions.html', context)


#Rankink
def rules(request):
    categories = Category.objects.all()
    return render(request, 'html/rules.html',{'categories': categories})



def playing(request, category_id, level_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, pk=category_id)
    level = get_object_or_404(Level, pk=level_id)
    questions = Question.objects.filter(category=category,level=level).order_by('category').order_by('level')
    score = 0
    total = questions.count()

    for question in questions:
        selected_answer = request.POST.get(f'pergunta_{question.id}')
        if selected_answer:
            answer = Answer.objects.get(id=selected_answer)
            print(answer.answer)
            if answer.is_correct:
                score += 1
                print(score)
                print(total)
                logging.info(score)
                print(selected_answer)
    return redirect('detlog:list_of_questions', category.pk, level.pk,total,score)#HttpResponseRedirect(reverse('detlog:list_of_questions', args=(form,)))#render(request, 'html/questions.html', {'form': form})



#@login_required
def error(request, category_id, level_id):
    
    categories = Category.objects.all()
    category = get_object_or_404(Category, pk=category_id)
    level = get_object_or_404(Level, pk=level_id)
    questions = Question.objects.filter(category=category,level=level).order_by('category').order_by('level')
    paginator = Paginator(questions,1)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        questions_in_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        questions_in_page = paginator.page(paginator.num_pages)

    for q in questions_in_page:
        question = get_object_or_404(Question, pk=q.pk)
        if not question:
             return render(request,'html/no_questions.html',{'category':category,'level': level, 'questions': questions_in_page,'categories': categories,'answer': answer, 'form': form})
        context = {'category':category,'level': level, 'questions': questions_in_page,'categories': categories,'question':question,'answer': answer, 'form': form}
    if not questions_in_page:
        return render(request, 'html/no_questions.html',{'category':category,'level': level, 'questions': questions_in_page,'categories': categories,'answer': answer, 'form': form})

    if request.method == 'POST':
        form = AnswersForm(request.POST)
        if form.is_valid():
            answer = form.cleaned_data['answer']
            score = 0
            for q in questions_in_page:


                logging.debug(q.questions.all())
                #correct_answer = question.questions.all()
                #if request.POST.get('answer.is_correct')==correct_answer.answer.is_correct:
                score += 1
            time = int(request.POST.get('time', 0))
            Player.objects.create(player_name=request.user, category=category, level=level, score=score, time=time)
            return render(request, 'html/questions.html', context) #redirect('detlog:list_of_questions', category_id=category.pk, nivel_id=level.pk)
    else:
        form = AnswersForm()
    return render(request, 'html/questions.html', {'context':context,'answer': answer, 'form': form})



 #for question in questions:
 #       correct_answer = Answer.objects.get(question=question, is_correct=True)
 #       try:
 #           selected_answer = question.questions.get(pk=request.POST['answer'])
 #       except (KeyError, Answer.DoesNotExist):
 #           return render(request, 'html/ranking.html',{'question':correct_answer,'error_message':'Mais um erro. Não encontrado...'})
 #       else:
 #           selected_answer.score+=1
#            selected_answer.time = int(request.POST.get('time', 0))
#            selected_answer.save()
#        Player.objects.create(player_name=request.user, category=category, level=level)
#        return redirect('detlog:ranking', category_id=category.pk, nivel_id=level.pk)
#    return render(request, 'html/ranking.html', {'category': category, 'level': level,'categories':categories})



def submit(request, question_id):
    question = Question.objects.get(pk=question_id)
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
    
    if selected_choice.i:
        score, created = Player.objects.get_or_create(user=request.user)
        score.score += 1
        score.save()
        
    return HttpResponseRedirect('/html/')


def scores(request):
    scores = Player.objects.all().order_by('-score')
    return render(request, 'html/scores.html', {'scores': scores})


#Rules
def ranking(request):
    categories = Category.objects.all()
    return render(request, 'html/ranking.html',{'categories': categories})


#def ranking(request):
#    ranking = Player.objects.values('user__username').annotate(total_pontos=models.Sum('score')).order_by('-total')
#    return render(request, 'html/ranking.html', {'ranking': ranking})


def processing_answers(request, level_id):
    level = get_object_or_404(Level, id=level_id)
    questions = Question.objects.filter(level=level)
    score = 0
    total = quetions.count()

    for quetion in quetions:
        selected_answer = request.POST.get(f'pergunta_{quetion.id}')
        if selected_answer:
            answer = Answer.objects.get(id=selected_answer)
            if answer.is_correct:
                score += 1

    return render(request, 'html/answers.html', {'level': level, 'score': score, 'total': total})

















##Ja refinado
def resultados(request, category_id, level_id):
    category = get_object_or_404(Category, pk=category_id)
    level = get_object_or_404(Level, pk=level_id)
    results = Answer.objects.filter(category=category, level=level).order_by('-score', 'time')
    return render(request, 'html/result.html', {'category': category, 'level': category, 'results': results})






def resever_list_of_question(request, category_id,level_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, pk=category_id)
    level = get_object_or_404(Level, pk=level_id)
    questions = Question.objects.filter(category=category,level=level)
    if not questions:
        return render(request, 'html/no_questions.html', {'category':category,'level': level, 'questions': questions,'categories': categories})
    return render(request, 'html/questions.html', {'category':category,'level': level, 'questions': questions,'categories': categories})


'''
for post in posts:
        if post.likes.filter(id=request.user.id).exists():
            post.liked = True
            post.save()
        else:
            post.liked = False
            post.save()
'''