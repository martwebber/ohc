from django import forms
from django.forms import ModelForm
# from django.contrib.auth.forms import UserCreationForm
from .models import Question, Answer, Post
# from django.contrib.auth.models import User


class QuestionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['body'].required = True
        self.fields['tags'].required = False

    title = forms.CharField(
        label='Title', min_length=10, max_length=100, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Enter a title', 'id': 'form-title'}))

    body = forms.CharField(
        label='Body', min_length=30, max_length=100, widget=forms.Textarea(
            attrs={'rows': 4, 'class': 'form-control mb-3', 'placeholder': 'Enter more details', 'id': 'form-body'}))

    tags = forms.CharField(
        label='Tags', widget=forms.TextInput(
            attrs={'rows': 1, 'class': 'form-control mb-3', 'placeholder': 'Enter your tags', 'id': 'form-tags'}))

    class Meta:
        model = Question
        fields = ('title', 'body', 'tags')


class AnswerForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['answer'].required = True
    answer = forms.CharField(
        label='', min_length=30, max_length=100, widget=forms.Textarea(
            attrs={'rows': 2, 'class': 'form-control mb-3', 'placeholder': 'Type your answer here...', 'id': 'form-answer'}))

    class Meta:
        model = Answer
        fields = ('answer',)


class PostForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['body'].required = True
        self.fields['tags'].required = False

    title = forms.CharField(
        label='Title', min_length=10, max_length=100, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Enter a title', 'id': 'form-title'}))

    body = forms.CharField(
        label='Body', widget=forms.Textarea(
            attrs={'rows': 12, 'class': 'form-control mb-3', 'placeholder': 'Share our story', 'id': 'form-body'}))

    tags = forms.CharField(
        label='Tags', widget=forms.TextInput(
            attrs={'rows': 1, 'class': 'form-control mb-3', 'placeholder': 'Enter your tags', 'id': 'form-tags'}))

    class Meta:
        model = Post
        fields = ('title', 'body', 'tags')
