from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth import login,logout,authenticate
from django.core.exceptions import ObjectDoesNotExist
from game.models import*
from .forms import*



def quiz_result_questions(request,question_answered_pk):
    title = 'Resultado'
    answered = get_object_or_404(Result,pk=question_answered_pk)
    context = {'answered':answered,'title':title}
    return render(request,'html/quiz_results.html',context)


#Player Playing
def quiz_play(request):
    quiz_user, created = QuizUser.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        answer_id = request.POST.get('answer_id')
        question_answered = quiz_user.choices.select_related('question').get(question_id=question_id)

        try:
            selected_option = question_answered.question.questions_options.get(pk=answer_id)
        except ObjectDoesNotExist:
            Http404
        quiz_user.validate_attempt(question_answered,selected_option)
        return redirect('quizz:quiz_result_questions',question_answered.pk)

    else:
        question = quiz_user.get_new_questions()
        if question is not None:
            quiz_user.create_attempts(question)
        context = {'question':question}
    return render(request,'html/quiz_play.html',context)




#Player Home Route View
def quiz_user_home(request):
    return render(request,'html/quiz_user_home.html',)


#Player Logout Route view
def quiz_logout(request):
    logout(request)
    return redirect('quizz:index')



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
    print(form)
    return render(request,'html/quiz_user.html',context)


#Index is working perfect
def index(request):
    categories = Category.objects.all()
    return render(request,'html/index.html', {'categories': categories})

##List of levels are working perfect
def list_of_levels(request, category_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, pk=category_id)
    return render(request, 'html/quizz.html', {'category': category,'categories': categories})


def quizz_view(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    questions = []
    for q in category.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.answer_text)
        questions.append({str(q):answers})
    return JsonResponse({
        'data':questions,
        'time':category.time
    })



#List of questions are working perfect
def list_of_questions(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    questions = Question.objects.filter(category=category).order_by('category')

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
             return render(request,'html/no_questions.html',{'category':category,'questions': questions_in_page,})
        context = {'category':category, 'questions': questions_in_page,'question':question}
    if not questions_in_page:
        return render(request, 'html/no_questions.html',{'category':category,'questions': questions_in_page,})
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
    rules = Config.objects.all()
    context = {'categories': categories,'rules':rules}
    return render(request, 'html/rules.html',context)


def playing(request, category_id):
    categories = Category.objects.all()
    return render(request, 'html/quizz.html',{'categories': categories})

def play(request, category_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, pk=category_id)
    #level = get_object_or_404(Level, pk=level_id)
    questions = Question.objects.filter(category=category).order_by('category')#.order_by('level')
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
                print(selected_answer)
    return redirect('quizz:list_of_questions', category.pk)#HttpResponseRedirect(reverse('detlog:list_of_questions', args=(form,)))#render(request, 'html/questions.html', {'form': form})



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



 
#Rules
def ranking(request):
    categories = Category.objects.all()
    total_quiz_user = QuizUser.objects.order_by('-total_score')[:10]
    user_counter = total_quiz_user.count()
    context = {'categories': categories,'user_counter':user_counter,'total_quiz_user':total_quiz_user}
    return render(request, 'html/ranking.html',context)




#def ranking(request):
#    ranking = Player.objects.values('user__username').annotate(total_pontos=models.Sum('score')).order_by('-total')
#    return render(request, 'html/ranking.html', {'ranking': ranking})

















##Ja refinado
def resultados(request, category_id, level_id):
    category = get_object_or_404(Category, pk=category_id)
    level = get_object_or_404(Level, pk=level_id)
    results = Answer.objects.filter(category=category, level=level).order_by('-score', 'time')
    return render(request, 'html/result.html', {'category': category, 'level': category, 'results': results})


