from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


# Topic
class Topic(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    topic = models.CharField(max_length=100,)
    follow = models.ManyToManyField(CustomUser, blank=True, related_name='follow')


    def __str__(self):
        return self.topic

    
# Question Model
class Question(models.Model):
    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    topic = models.ForeignKey("Topic", null=True, blank=True, on_delete=models.DO_NOTHING)
    body = models.TextField()
    tags = models.TextField(default='')
    favourites = models.ManyToManyField(
        CustomUser, related_name='favourite', default=None, blank=True)
    add_time = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()  # default manager
    newmanager = NewManager()  # custom manage
    def __str__(self):
        return self.title

# Answer Model
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    answer = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(CustomUser, blank=True, related_name='dislikes')

    def __str__(self):
        return self.answer
