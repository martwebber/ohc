from django.contrib import admin
from .models import Question, Answer, Topic, CustomUser
# from accounts.models import 
from django.contrib.auth.models import User


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')
    search_fields = ('title', 'body')


admin.site.register(Question, QuestionAdmin)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'user')
    search_fields = ('answer', )


admin.site.register(Answer, AnswerAdmin)



#class TopicAdmin(admin.ModelAdmin):
 #   list_display = ('topic', 'user')


admin.site.register(Topic)
