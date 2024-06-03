from django.contrib import admin
from game.models import*



#Register Categories Admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    list_display_links = ('category_name',)
    fields = ('category_name',)
    search_fields = ('category_name',)
    ordering = ['category_name']
    #list_editable = ('category_name',)
admin.site.register(Category,CategoryAdmin)


#Register Levels Admin
class LevelAdmin(admin.ModelAdmin):
    list_display = ('id','level_name',)
    list_display_links = ('level_name',)
    fields = ('level_name',)
    search_fields = ('level_name',)
    ordering = ['level_name']
admin.site.register(Level,LevelAdmin)


#Register Questions Admin InLines

class AnswerInLine(admin.TabularInline):
    model = Answer
    extra = 4

#Register Questions Admin
class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerInLine,
    ]
    list_display = ('question_text','category','level',)
    list_display_links = ( 'question_text','category','level',)
    fields=('question_text','category','level')
    search_fields = ('question_text',)
    autocomplete_fields =('category','level',)
    ordering = ['question_text','category']
admin.site.register(Question,QuestionAdmin)


#Register Answers Admin
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('quetion','answer','is_correct')
    list_display_links = ('quetion','answer','is_correct')
    fields = ('quetion','answer','is_correct')
    search_fields = ('answer',)
    autocomplete_fields = ('quetion',)
    ordering = ['quetion']
    unique_together = ("quetion", "answer")
admin.site.register(Answer,AnswerAdmin)


#Register Players Admin
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('player_name','score','time','category','level')
    list_display_links = ('player_name','score','time','category','level')
    fields = ('player_name','score','time','category','level')
    autocomplete_fields = ('category','level')
    ordering = ['player_name']
admin.site.register(Player,PlayerAdmin)