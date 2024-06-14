from django.contrib import admin
from game.models import *
from game.forms import *

class DifficultyAdmin(admin.ModelAdmin):
    list_display = ('difficulty_text',)
    list_display_links = ('difficulty_text',)
    fields = ('difficulty_text',)
    search_fields = ('difficulty_text',)
    ordering = ['difficulty_text']
admin.site.register(Difficulty,DifficultyAdmin)

#Register Categories Admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    list_display_links = ('category_name',)
    fields = ('category_name',)
    search_fields = ('category_name',)
    ordering = ['category_name']
    #list_editable = ('category_name',)
admin.site.register(Category,CategoryAdmin)



#Register Questions Admin InLines

class AnswerInLine(admin.TabularInline):
    model = Answer
    #max_num = Answer.MAXIM_ANSWER = 4
    #extra = 4
    formset = AnswerInlineFormer

#Register Questions Admin
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInLine]
    list_display = ('question_text','category','difficulty','max_score',)
    list_display_links = ( 'question_text','category','difficulty','max_score',)
    fields=('question_text','category','difficulty','max_score',)
    search_fields = ('question_text','difficulty','category',)
    autocomplete_fields =('category','difficulty',)
    ordering = ['question_text','category','difficulty']
admin.site.register(Question,QuestionAdmin)


#Register Answers Admin
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question','answer_text','is_correct')
    list_display_links = ('question','answer_text','is_correct')
    fields = ('question','answer_text','is_correct')
    search_fields = ('answer_text',)
    autocomplete_fields = ('question',)
    ordering = ['question']
    unique_together = ('question', 'answer_text')
admin.site.register(Answer,AnswerAdmin)


class QuizUserAdmin(admin.ModelAdmin):
    list_display = ('user','total_score',)
    list_display_links = ('user','total_score',)
    fields = ('user','total_score',)
    autocomplete_fields = ('user',)
    search_fields = ('user','total_score',)
    ordering = ['total_score']
admin.site.register(QuizUser,QuizUserAdmin)


#Register Players Admin
class ResultAdmin(admin.ModelAdmin):
    list_display = ('quiz_user','category','difficulty','question','answer','score','time')
    list_display_links = ('quiz_user','category','difficulty','question','answer','score','time')
    fields = ('quiz_user','category','difficulty','question','answer','score','time')
    search_fields = ('quiz_user','category','difficulty','question','answer')
    autocomplete_fields = ('quiz_user','category','question','answer','difficulty',)
    ordering = ['quiz_user']
admin.site.register(Result,ResultAdmin)


class ConfigAdmin(admin.ModelAdmin):
    list_display = ('rule',)
    list_display_links = ('rule',)
    fields = ('rule',)
    search_fields = ('rule',)
    ordering = ['rule']
admin.site.register(Config,ConfigAdmin)