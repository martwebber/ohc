from django import forms
from django.db import models
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.generic.edit import UpdateView
from .forms import QuestionForm, AnswerForm, TopicForm
from .models import Question, Answer, Topic
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse

# from accounts.decorators import admin_only, allowed_users


# Homepage
def home(request):
    user = request.user
    if not request.user.is_authenticated:
        questions = Question.objects.all()
        topics = Topic.objects.all()
    else:
        topics = Topic.objects.filter(follow=user.id)
        questions_user = Question.objects.all()
        
        questions = Question.objects.annotate(total_answers=Count('answer__question')).filter(Q(topic__in=topics) | Q(user=user))
        paginator = Paginator(questions, 5)
        page_num = request.GET.get('page', 1)
        questions = paginator.page(page_num)
    context = {'questions': questions, 'topics': topics, }
    return render(request, 'home.html', context)

    
# Ask 
@login_required
def ask_question(request):
    form = QuestionForm
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question_form = question_form.save(commit=False)
            question_form.user = request.user
            question_form.save()
            messages.success(request, 'Question has been added.')
            return redirect('/')
    context = {'form': form}
    return render(request, 'ask-question.html', context)


# Single question
def single_question_page(request, id):
    post = get_object_or_404(Question, id=id)
    fav = bool
    if post.favourites.filter(id=request.user.id).exists():
        fav = True
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
    context = {'question': question, 'tags': tags, 'answers': answers, 'answerForm': answerform, 'fav':fav}
    return render(request, 'single-question.html', context)


@login_required
# @allowed_users(allowed_roles=['admin'])
def deleteQuestion(request, pk):
    question = Question.objects.get(id=pk)
    if request.method == 'POST':
        question.delete()
        return redirect('/')
    context = {'question':question}
    return render(request, 'single-question.html', context)



@login_required
def updateQuestion(request, id):
    question = Question.objects.get(id=id)
    form = QuestionForm(instance=question)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Question has been updated.')
            return redirect('main:home')
            
    context = {'form': form}
    return render(request, 'update-question.html', context)


def questionsPage(request):
    questions = Question.objects.all().order_by('-add_time')
    #questions = Question.objects.annotate(total_answers=Count('answer__question')).order_by('-total_answers')
    paginator = Paginator(questions, 5)
    page_num = request.GET.get('page', 1)
    questions = paginator.page(page_num)
    context = {'questions': questions}
    return render(request, 'questions.html', context)


# Answer 
@login_required(login_url='login')
def deleteAnswer(request, pk):
    answer = Answer.objects.get(id=pk)
    if request.method == 'POST':
        answer.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    context = {}
    return render(request, 'single-question.html', context)


@login_required
# @allowed_users(allowed_roles=['admin'])
def updateAnswer(request, pk):
    # answer = get_object_or_404(id=pk)
    answer = Answer.objects.get(id=pk)
    form = AnswerForm(instance=answer)
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            # messages.success(request, 'Question has been updated.')
        else:
            form = AnswerForm(instance=answer)
    else:
        form = AnswerForm(instance=answer)
    context = {'form': form}
    return render(request, 'single-question.html', context)


@login_required
def favourite_list(request):
    new = Question.newmanager.filter(favourites=request.user)
    return render(request,
                  'favourites.html',
                  {'new': new})


@login_required
def favourite_add(request, id):
    post = get_object_or_404(Question, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

# Questions according to tag
def tag(request,tag):
    quests=Question.objects.filter(tags__icontains=tag).order_by('-id')
    paginator=Paginator(quests,10)
    page_num=request.GET.get('page',1)
    quests=paginator.page(page_num)
    return render(request,'tag.html',{'quests':quests,'tag':tag})


# Tags Page
def tags(request):
    quests=Question.objects.all()
    tags=[]
    for quest in quests:
        qtags=[tag.strip() for tag in quest.tags.split(',')]
        for tag in qtags:
            if tag not in tags:
                tags.append(tag)
    # Fetch Questions
    tag_with_count=[]
    for tag in tags:
        tag_data={
            'name':tag,
            'count':Question.objects.filter(tags__icontains=tag).count()
        }
        tag_with_count.append(tag_data)
    return render(request,'tags.html',{'tags':tag_with_count})


# Tags Page
def topics(request):
    topics=Topic.objects.all()
   # quests=Question.objects.annotate(total_questions=Count('topic__question')).filter(topic=topic).order_by('-add_time')
    topicForm = TopicForm
    # followers = topic.follow.all()

    context = {'topics':topics, 'topicForm':topicForm}

    return render(request,'topics.html', context)

# Questions according to tag
def topic(request,pk):
    topic = Topic.objects.get(pk=pk)
    quests=Question.objects.filter(topic=topic).order_by('-add_time')
    # topic = Topic.objects.get(pk=pk)
    user = request.user
    followers = topic.follow.all()
    number_of_followers = len(followers)


    if len(followers) == 0:
        is_following = False
    for follower in followers:
        if follower == request.user:
            is_following = True
            break
        else:
            is_following = False

    number_of_followers = len(followers)

    context = {
        'user': user,
        'topic': topic,
        'quests': quests,
        'number_of_followers': number_of_followers,
        'is_following': is_following,
    }

    return render(request,'topic.html',context)


def question_search(request):
    if request.method == 'GET':
        query = request.GET.get('q').lower()
        if query != '':
            questions = Question.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
            context = {'questions':questions}
            return render(request, 'search-results.html', context)
        else:
            context = {}
            return render(request, 'search-results.html', context)
    else:
        context = {}
        return render(request, 'search-results.html', context)
@login_required
def followTopic(request, pk):
        topic = Topic.objects.get(pk=pk)
        topic.follow.add(request.user)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def unfollowTopic(request, pk):
        topic = Topic.objects.get(pk=pk)
        topic.follow.remove(request.user)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def AddLike(request, pk):
        post = Answer.objects.get(pk=pk)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

@login_required
def AddDislike(request, pk):
    post = Answer.objects.get(pk=pk)

    is_like = False

    for like in post.likes.all():
        if like == request.user:
            is_like = True
            break

    if is_like:
        post.likes.remove(request.user)

    is_dislike = False

    for dislike in post.dislikes.all():
        if dislike == request.user:
            is_dislike = True
            break

    if not is_dislike:
        post.dislikes.add(request.user)

    if is_dislike:
        post.dislikes.remove(request.user)

    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)


class UpdateQuestionView(UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'update-question.html'

    #fields = ['title', 'topic', 'body', 'tags']


@login_required
def add_topic(request):
    form = TopicForm
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            #question_form.user = request.user
            form.save()
            #messages.success(request, 'Question has been added.')
            return redirect('/')
    context = {'topicForm': form}
    return render(request, 'topics.html', context)


def deleteTopic(request, pk):
    topic = Topic.objects.get(id=pk)
    if request.method == 'POST':
        topic.delete()
        return redirect('main:topics')
    context = {'topic':topic}
    return render(request, 'single-question.html', context)