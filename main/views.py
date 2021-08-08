from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import QuestionForm, AnswerForm, PostForm
from .models import Question, Answer, Comment, Post
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.decorators import login_required
# from accounts.decorators import admin_only, allowed_users


# Homepage
def home(request):
    if 'q' in request.GET:
        q = request.GET['q']
        questions = Question.objects.annotate(total_comments=Count('answer__comment')).filter(title__icontains=q).order_by('-id')
    else:
        questions = Question.objects.annotate(total_comments=Count('answer__comment')).all().order_by('-id')
    paginator = Paginator(questions, 5)
    page_num = request.GET.get('page', 1)
    questions = paginator.page(page_num)
    context = {'questions': questions}
    return render(request, 'home.html', context)


# Homepage
def posts_page(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 5)
    page_num = request.GET.get('page', 1)
    posts = paginator.page(page_num)
    context = {'posts': posts}
    return render(request, 'posts-page.html', context)


# Create Post
def create_post(request):
    form = PostForm
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post_form = post_form.save(commit=False)
            post_form.user = request.user
            post_form.save()
            messages.success(request, 'Your story has been posted. Thank you for sharing.')
            return redirect('posts_page')
    context = {'form': form}
    return render(request, 'create-post.html', context)


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


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def deleteQuestion(request, pk):
    question = Question.objects.get(id=pk)
    if request.method == 'POST':
        question.delete()
        return redirect('/')
    context = {'question': question}
    return render(request, 'delete.html', context)


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def update_question(request, pk):
    question = Question.objects.get(id=pk)
    form = QuestionForm(instance=question)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Question has been updated.')
            return redirect('/')
    context = {'form': form}
    return render(request, 'ask-question.html', context)
