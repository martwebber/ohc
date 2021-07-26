from django.db import models
from accounts.models import CustomUser


# Question Model
class Question(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    body = models.TextField()
    tags = models.TextField(default='')
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Answer Model
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    answer = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer


# Comment
class Comment(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comment_user')
    comment = models.TextField(default='')
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


# UpVotes
class UpVote(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='upvote_user')


# DownVotes
class DownVote(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='downvote_user')
