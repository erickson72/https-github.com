from django.db import models

# Create your models here.

class Category(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True,serialize=False, verbose_name='ID')
    category_name = models.CharField(verbose_name='Categoria', max_length=40)
    
    def __str__(self) -> str:
        return f"{self.category_name}"
    
class Level(models.Model):
    id = models.AutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID',)
    level_name = models.CharField(verbose_name='Nível',max_length=40,)
    
    def __str__(self) -> str:
        return f"{self.level_name}"
    
class Question(models.Model):
    id = models.AutoField(verbose_name='ID',auto_created=True, primary_key=True,serialize=False,)
    question_text = models.TextField(verbose_name='Questão',max_length=255,)
    category = models.ForeignKey(Category, verbose_name='Categoria',serialize=True,related_name='categories', related_query_name='question_category', on_delete=models.CASCADE)
    level = models.ForeignKey(Level, verbose_name='Nível',serialize=True,related_name='levels', related_query_name='question_level', on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.question_text}"
    
class Answer(models.Model):
    id = models.AutoField(verbose_name='ID',primary_key=True, serialize=False,auto_created=True)
    answer = models.TextField(verbose_name='Resposta', max_length=255)
    quetion = models.ForeignKey(Question,verbose_name='Questão',related_name='questions',related_query_name='question_answer', serialize=True, on_delete=models.CASCADE)
    is_correct = models.BooleanField(verbose_name='Correcta', default=False,)
    
    def __str__(self) -> str:
        return f"{self.answer}"
    
class Player(models.Model):
    id = models.AutoField(verbose_name='ID',auto_created=True,primary_key=True, serialize=False, unique=True)
    player_name = models.CharField(verbose_name='Nome',max_length=50)
    score = models.IntegerField()
    time = models.IntegerField()
    answer = models.ForeignKey(Answer,related_name='answers',related_query_name='player_answer',default=0,verbose_name='Resposta', on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.player_name}"