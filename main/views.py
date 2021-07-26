from django.shortcuts import render
# from django.core.paginator import Paginator
# from django.contrib import messages


# Homepage
def home(request):
    return render(request, 'home.html')


# Ask question
def ask_question(request):

    return render(request, 'ask-question.html')


# Answer
def answer(request):
    return render(request, 'single-question.html')
