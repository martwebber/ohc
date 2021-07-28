from django.shortcuts import render, redirect
from .forms import QuestionForm


# from django.core.paginator import Paginator
from django.contrib import messages


# Homepage
def home(request):
    return render(request, 'home.html')


# Ask question
def ask_question(request):
    form = QuestionForm
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question_form = question_form.save(commit=False)
            question_form.user = request.user
            question_form.save()
            messages.success(request, 'Question has been added.')
            return redirect('home')
    context = {'form': form}
    return render(request, 'ask-question.html', context)


# Answer
def answer(request):
    return render(request, 'single-question.html')
