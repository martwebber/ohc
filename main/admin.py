from django.contrib import admin
from .models import Question, Answer, Comment, DownVote, UpVote
# from accounts.models import CustomUser


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')
    search_fields = ('title', 'body')


admin.site.register(Question, QuestionAdmin)


admin.site.register(Answer)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('answer', 'comment')


admin.site.register(Comment, CommentAdmin)


class UpvoteAdmin(admin.ModelAdmin):
    list_display = ('answer', 'user')


admin.site.register(UpVote, UpvoteAdmin)


class DownvoteAdmin(admin.ModelAdmin):
    list_display = ('answer', 'user')


admin.site.register(DownVote, DownvoteAdmin)
