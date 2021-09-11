from accounts.models import CustomUser
from django import forms
from django.forms import ModelForm
# from django.contrib.auth.forms import UserCreationForm
from .models import Question, Answer, Topic
# from django.contrib.auth.models import User


class QuestionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['topic'].required = False
        self.fields['body'].required = False
        self.fields['tags'].required = False

    title = forms.CharField(
        label='Title', min_length=10, max_length=100, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Enter a title', 'id': 'form-title'}))

    body = forms.CharField(
        label='Body', min_length=30, max_length=1000, widget=forms.Textarea(
            attrs={'rows': 4, 'class': 'form-control mb-3', 'placeholder': 'Enter more details', 'id': 'form-body'}))
    topic = forms.ModelChoiceField(queryset=Topic.objects.all().order_by('topic'))
    tags = forms.CharField(
        label='Tags', widget=forms.TextInput(
            attrs={'rows': 1, 'class': 'form-control mb-3', 'placeholder': 'Enter your tags', 'id': 'form-tags'}))

    class Meta:
        model = Question
        fields = ('title', 'topic','body', 'tags')


# Answer form
class AnswerForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['answer'].required = True
    answer = forms.CharField(
        label='', min_length=30, max_length=1000, widget=forms.Textarea(
            attrs={'rows': 2, 'class': 'form-control mb-3', 'placeholder': 'Type your answer here...', 'id': 'form-answer'}))

    class Meta:
        model = Answer
        fields = ('answer',)


# Topic form
class TopicForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic'].required = True
        self.fields['user'].required = True

    topic = forms.CharField(
        label='Topic', widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Enter a Topic', 'id': 'form-title'}))
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all().order_by('username'))


    class Meta:
        model = Topic
        fields = ('topic','user')



class PostSearchForm(forms.Form):
    q = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['q'].label = 'Search For'
        self.fields['q'].widget.attrs.update(
            {'class': 'form-control'})                            