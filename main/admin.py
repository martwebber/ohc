from django.contrib import admin
from .models import Question, Answer, Topic
# from accounts.models import CustomUser


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')
    search_fields = ('title', 'body')


admin.site.register(Question, QuestionAdmin)


admin.site.register(Answer)



#class TopicAdmin(admin.ModelAdmin):
 #   list_display = ('topic', 'user')


admin.site.register(Topic)
