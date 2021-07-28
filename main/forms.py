from django import forms
from django.forms import ModelForm
# from django.contrib.auth.forms import UserCreationForm
from .models import Question
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
            attrs={'rows': 10, 'class': 'form-control mb-3', 'placeholder': 'Enter more details', 'id': 'form-body'}))

    tags = forms.CharField(
        label='Tags', widget=forms.TextInput(
            attrs={'rows': 1, 'class': 'form-control mb-3', 'placeholder': 'Enter your tags', 'id': 'form-tags'}))

    class Meta:
        model = Question
        fields = ('title', 'body', 'tags')