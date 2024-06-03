from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from .models import*
from .forms import*
from django.contrib.auth import views as auth_views



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
    questions = Question.objects.filter(category=category,level=level)
    
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



#Jogar
def playing(request,category_id,level_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, pk=category_id)
    level = get_object_or_404(Level, pk=level_id)
    questions = Question.objects.filter(category=category,level=level)
    
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


















def submit(request, question_id):
    question = Question.objects.get(pk=question_id)
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
    
    if selected_choice.i:
        score, created = Player.objects.get_or_create(user=request.user.username)
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

    return render(request, 'html/result.html', {'level': level, 'score': score, 'total': total})










@login_required
def quiz(request, category_id, level_id):
    category = get_object_or_404(Category, pk=category_id)
    nivel = get_object_or_404(Level, pk=level_id)
    quetions = Question.objects.filter(category=category, level=level)
    if request.method == 'POST':
        form = AnswersForm(request.POST)
        if form.is_valid():
            answers = form.cleaned_data['answers']
            score = 0
            for pergunta in quetions:
                resposta_correta = Answer.objects.get(pergunta=pergunta, correta=True)
                if respostas.get(str(pergunta.id)) == str(resposta_correta.id):
                    pontuacao += 1
            tempo = int(request.POST.get('tempo', 0))
            Answer.objects.create(usuario=request.user, categoria=categoria, nivel=nivel, pontuacao=pontuacao, tempo=tempo)
            return redirect('resultados', categoria_id=categoria.id, nivel_id=nivel.id)
    else:
        form = RespostaForm()
    return render(request, 'quiz/quiz.html', {'categoria': categoria, 'nivel': nivel, 'perguntas': perguntas, 'form': form})





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