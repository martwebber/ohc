from django.contrib import admin
from .models import Question, Answer, Comment, DownVote, UpVote, Post, Topic
# from accounts.models import CustomUser


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')
    search_fields = ('title', 'body')


admin.site.register(Question, QuestionAdmin)


admin.site.register(Answer)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('answer', 'comment')


admin.site.register(Comment, CommentAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')


admin.site.register(Post, PostAdmin)


class TopicAdmin(admin.ModelAdmin):
    list_display = ('topic', 'user')


admin.site.register(Topic, TopicAdmin)


class UpvoteAdmin(admin.ModelAdmin):
    list_display = ('answer', 'user')


admin.site.register(UpVote, UpvoteAdmin)


class DownvoteAdmin(admin.ModelAdmin):
    list_display = ('answer', 'user')


admin.site.register(DownVote, DownvoteAdmin)
