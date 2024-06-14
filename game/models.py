from django.db import models
from django.contrib.auth.models import User
import random


# Create your models here.

class Difficulty(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
    difficulty_text = models.CharField(verbose_name='Nível', max_length=40)

    class Meta:
        verbose_name = ("Nével")
        verbose_name_plural = ("Níveis")

    def __str__(self):
        return f"{self.difficulty_text}"

class Category(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
    category_name = models.CharField(verbose_name='Categoria', max_length=40)

    
    class Meta:
        verbose_name = ("Categoria")
        verbose_name_plural = ("Categorias")

    def __str__(self) -> str:
        return f"{self.category_name}"
    
    def get_questions(self):
        return self.question_set.all()#[:self.number_of_question]

    
class Question(models.Model):
    
    NUMBER_OF_ACCEPTED_ANSWER = 1

    id = models.AutoField(verbose_name='ID',auto_created=True, primary_key=True)
    question_text = models.TextField(verbose_name='Questão')
    category = models.ForeignKey(Category, verbose_name='Categoria',  on_delete=models.CASCADE)
    difficulty = models.ForeignKey(Difficulty, verbose_name='Nível',  on_delete=models.CASCADE)
    max_score = models.DecimalField(verbose_name='Pontos máximos',decimal_places=2,max_digits=10, default=5)
    created = models.DateTimeField(auto_now_add=True)
   
    class Meta:
        verbose_name = ("Pergunta")
        verbose_name_plural = ("Perguntas")

    
    def __str__(self) -> str:
        return f"{self.question_text}"
    
    def get_answers(self):
        return self.answer_set.all()
  
    
class Answer(models.Model):
    #MAXIM_ANSWER = 4
    id = models.AutoField(verbose_name='ID',primary_key=True, auto_created=True)
    answer_text = models.TextField(verbose_name='Resposta', max_length=255)
    question = models.ForeignKey(Question,verbose_name='Questão', related_name='questions_options',on_delete=models.CASCADE)
    is_correct = models.BooleanField(verbose_name='Correcta', default=False,)
    
    def __str__(self) -> str:
        return f"{self.answer_text}"
    
    class Meta:
        verbose_name = ("Resposta")
        verbose_name_plural = ("Respostas")


class QuizUser(models.Model):
    id = models.AutoField(verbose_name='ID',primary_key=True, auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Jogador')
    total_score = models.DecimalField(decimal_places=2,default=0, max_digits=10, verbose_name='Total de Pontos',null=True)

    class Meta:
        verbose_name = ("Jogador")
        verbose_name_plural = ("Jogadores")

    def __str__(self):
        return f"{self.user.username}"
    
    def create_attempts(self,question):
        attempt = Result(question=question,quiz_user=self)
        attempt.save()
    
    def get_new_questions(self):
        answered = Result.objects.filter(quiz_user=self).values_list('question__pk',flat=True)
        remaining_questions = Question.objects.exclude(pk__in=answered)
        if not remaining_questions.exists():
            return None
        return random.choice(remaining_questions)
    
    def validate_attempt(self,question_answered,answer_selected):
        if question_answered.question_id != answer_selected.question_id:
            return
        question_answered.answer_selected = answer_selected
        if answer_selected.is_correct is True:
            question_answered.is_correct = True
            question_answered.score = answer_selected.question.max_score
            question_answered.category = answer_selected.question.category
            question_answered.difficulty = answer_selected.question.difficulty
            question_answered.answer = answer_selected
        else:
            question_answered.answer = answer_selected
        question_answered.save()
        self.update_score()


    def update_score(self):
        score_updated = self.choices.filter(is_correct=True).aggregate(models.Sum('score'))['score__sum']
        self.total_score = score_updated
        self.save()
        

    


    
class Result(models.Model):
    id = models.AutoField(verbose_name='ID',primary_key=True, auto_created=True)
    quiz_user = models.ForeignKey(QuizUser,verbose_name='Jogador', on_delete=models.CASCADE,related_name='choices')
    question = models.ForeignKey(Question,verbose_name='Questão', on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey(Answer, verbose_name='Resposta', on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, verbose_name='Categoria',on_delete=models.CASCADE, null=True)
    difficulty = models.ForeignKey(Difficulty, verbose_name='Nível',  on_delete=models.CASCADE, null=True)
    is_correct = models.BooleanField(verbose_name='Correcta', default=False,null=False)
    score = models.IntegerField(default=0)
    time = models.IntegerField(help_text="Tempo em segundos",default=0)

      
    def __str__(self) -> str:
        return f"{self.quiz_user.user.username}"
        
    
    class Meta:
        verbose_name = ("Resultado")
        verbose_name_plural = ("Resultados")


class Config(models.Model):
    id = models.AutoField(verbose_name='ID',primary_key=True, auto_created=True)
    rule = models.TextField(null=True, verbose_name='Regra')

    class Meta:
        verbose_name = ("Regra")
        verbose_name_plural = ("Regras")

    def __str__(self):
        return self.rule