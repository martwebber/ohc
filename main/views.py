from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import QuestionForm, AnswerForm
from .models import Question, Answer, Comment
from django.views.decorators.csrf import csrf_exempt


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
            return redirect('ask_question')
    context = {'form': form}
    return render(request, 'ask-question.html', context)


# Single question
def single_question_page(request, id):
    question = Question.objects.get(pk=id)
    tags = question.tags.split(',')
    answers = Answer.objects.filter(question=question)
    answerform = AnswerForm
    if request.method == 'POST':
        answerContent = AnswerForm(request.POST)
        if answerContent.is_valid():
            answer = answerContent.save(commit=False)
            answer.question = question
            answer.user = request.user
            answer.save()
            messages.success(request, 'Your answer has been submitted.')
    context = {'question': question, 'tags': tags, 'answers': answers, 'answerForm': answerform}
    return render(request, 'single-question.html', context)


# Save Comment
@csrf_exempt
def save_comment(request):
    if request.method == 'POST':
        comment = request.POST['comment']
        answerId = request.POST['answerId']
        answer = Answer.objects.get(pk=answerId)
        user = request.user
        Comment.objects.create(
            answer=answer,
            comment=comment,
            user=user
            )
        context = {'bool': True}
        return JsonResponse(context)
