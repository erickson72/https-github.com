from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True,serialize=False, verbose_name='ID')
    category_name = models.CharField(verbose_name='Categoria', max_length=40)
    
    def __str__(self) -> str:
        return f"{self.category_name}"
    
    class Meta:
        verbose_name = ("Categoria")
        verbose_name_plural = ("Categorias")
    
class Level(models.Model):
    id = models.AutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID',)
    level_name = models.CharField(verbose_name='Nível',max_length=40,)
    
    def __str__(self) -> str:
        return f"{self.level_name}"
    
    class Meta:
        verbose_name = ("Nível")
        verbose_name_plural = ("Níveis")
        
    
class Question(models.Model):
    id = models.AutoField(verbose_name='ID',auto_created=True, primary_key=True,serialize=False,)
    question_text = models.TextField(verbose_name='Questão')
    category = models.ForeignKey(Category, verbose_name='Categoria',serialize=True,related_name='categories', related_query_name='question_category', on_delete=models.CASCADE)
    level = models.ForeignKey(Level, verbose_name='Nível',serialize=True,related_name='levels', related_query_name='question_level', on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Pergunta")
        verbose_name_plural = ("Perguntas")

    
    def __str__(self) -> str:
        return f"{self.question_text}"
    
    @property
    def question_count(self):
        return Question.objects.filter(level=self.level,category=self.category).count()
  

    
    
    
class Answer(models.Model):
    id = models.AutoField(verbose_name='ID',primary_key=True, serialize=False,auto_created=True)
    answer = models.TextField(verbose_name='Resposta', max_length=255)
    question = models.ForeignKey(Question,verbose_name='Questão',related_name='questions',related_query_name='question_answer', serialize=True, on_delete=models.CASCADE)
    is_correct = models.BooleanField(verbose_name='Correcta', default=False,)
    
    def __str__(self) -> str:
        return f"{self.answer}"
    
    class Meta:
        verbose_name = ("Resposta")
        verbose_name_plural = ("Respostas")

    
class Player(models.Model):
    player_name = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='Jogador',related_name='playes')
    category = models.ForeignKey(Category, verbose_name='Categoria',serialize=True,related_name='category_players', related_query_name='player_category', on_delete=models.CASCADE)
    level = models.ForeignKey(Level, verbose_name='Nível',serialize=True,related_name='player_levels', related_query_name='player_level', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    time = models.IntegerField(help_text="Tempo em segundos",default=0)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.player_name} - {self.category} - {self.level} - {self.score}"
        
    
    class Meta:
        verbose_name = ("Resultado")
        verbose_name_plural = ("Resultados")