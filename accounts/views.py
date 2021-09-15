from django.db.models.deletion import PROTECT
from main.models import Topic, Question, Answer
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .models import CustomUser, Profile
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from .forms import CreateUserForm, UserEditForm, UserProfileForm, UserLoginForm, UserForm, ProfileForm, UserGroupForm
from main.forms import AnswerForm
from .token import account_activation_token
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from accounts.decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth import authenticate, login as auth_login, logout
from django.db.models import Count
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.urls import reverse
from datetime import timedelta
from django.utils.timezone import now
from django.shortcuts import get_object_or_404



# User Register
@unauthenticated_user
def register(request):
    if request.method == 'POST':
        registerForm = CreateUserForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            group = Group.objects.get(name='patients')
            user.groups.add(group)
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message, html_message=None)
            messages.success(request, 'Your account has been created. An activation link has been sent to your email.')
            context = {'registerForm': registerForm}
            return render(request, 'registration/register.html', context)
    else:
        registerForm = CreateUserForm()
    context = {'registerForm': registerForm}
    return render(request, 'registration/register.html', context)


# Activate
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        return redirect('login')
    else:
        return render(request, 'registration/activation_invalid.html')

@unauthenticated_user
def login(request):
    loginForm = UserLoginForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            if request.user.groups.filter(name="patients").exists():
                return redirect('main:home')
            if request.user.groups.filter(name="moderators").exists():
                return redirect('accounts:admin_dashboard')
            if request.user.groups.filter(name="admins").exists():
                return redirect('accounts:admin_dashboard')
            else:
                messages.info(request, 'Username or password is incorrect')

    context = {'loginForm': loginForm}
    return render(request,'registration/login.html', context)


# Profile
@login_required
def profile(request):
   # user = CustomUser.objects.get(pk=id)
    questions=Question.objects.filter(user=request.user).order_by('-id')
    answers=Answer.objects.filter(user=request.user).order_by('-id')
    topics=Topic.objects.filter(follow=request.user).order_by('-id')
    context = {'questions':questions, 'answers':answers, 'topics':topics}
    return render(request, 'registration/profile.html', context)


# Update user profile
# @login_required
# def edit_profile(request):
#     if request.method == 'POST':
#         user_form = UserEditForm(instance=request.user, data=request.POST)
#         if user_form.is_valid():
#             user_form.save()
#             messages.success(request, 'Your details have been updated successfully')
#             return redirect('accounts:profile')

#     else:
#         user_form = UserEditForm(instance=request.user)
#     context = {'user_form': user_form}
#     return render(request,'registration/update_profile.html',context)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)

        profile_form = UserProfileForm(
            request.POST, instance=request.user.profile)

        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('accounts:profile'))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)

    return render(request,
                  'registration/update_profile.html',
                  {'user_form': user_form, 'profile_form': profile_form})



class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile.html'

class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    profile_form = ProfileForm
    template_name = 'registration/update_profile.html'

    def post(self, request):

        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, file_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.error(request, 'Your profile is updated successfully!')
            return HttpResponseRedirect(reverse_lazy('accounts:profile'))

        context = self.get_context_data(
                                        user_form=user_form,
                                        profile_form=profile_form
                                    )

        return self.render_to_response(context)     

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


# Admin dashboard

@login_required(login_url='login')
@allowed_users(allowed_roles=['admins', 'moderators'])
def admin_dashboard(request):
    dt = now()
    latestQuestions = Question.objects.filter(add_time__range=(dt-timedelta(hours=24), dt))
    latestAnswers = Answer.objects.filter(add_time__range=(dt-timedelta(hours=24), dt))
    newUsers = CustomUser.objects.filter(date_joined__range=(dt-timedelta(hours=24), dt))
    context = {'latestQuestions': latestQuestions, 'latestAnswers': latestAnswers, 'newUsers': newUsers,}
    return render(request, 'admin/dashboard.html', context)


@login_required
def create_user(request):
    registerForm = CreateUserForm(request.POST)
    if registerForm.is_valid():
        user = registerForm.save(commit=False)
        user.email = registerForm.cleaned_data['email']
        user.set_password(registerForm.cleaned_data['password'])
        user.is_active = False
        user.save()
        group = Group.objects.get(name='patients')
        user.groups.add(group)
        current_site = get_current_site(request)
        subject = 'Activate your account'
        message = render_to_string('registration/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject=subject, message=message, html_message=None)
        messages.success(request, 'Your account has been created. An activation link has been sent to your email.')
        context = {'registerForm': registerForm}
        return render(request, 'registration/register.html', context)
    else:
        registerForm = CreateUserForm()
    context = {'registerForm': registerForm}
    return render(request, 'admin/all-users.html', context)



# Users Page
@login_required(login_url='login')
@allowed_users(allowed_roles=['admins', 'moderators'])
def users(request):
    users=CustomUser.objects.all().order_by('-date_joined')

    context = {'users':users, }

    return render(request,'admin/users.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def delete_user(request, id):
    user = CustomUser.objects.get(id=id)
    if request.method == 'POST':
        user.delete()
        return redirect('accounts:users')
    context = {'user':user}
    return render(request, 'users.html', context)


def questionsPage(request):
    questions = Question.objects.annotate(total_answers=Count('answer__question')).all().order_by('-add_time')
    #questions = Question.objects.annotate(total_answers=Count('answer__question')).order_by('-total_answers')
    paginator = Paginator(questions, 5)
    page_num = request.GET.get('page', 1)
    questions = paginator.page(page_num)
    context = {'questions': questions}
    return render(request, 'admin/questions.html', context)


@login_required
# @allowed_users(allowed_roles=['admin'])
def delete_question(request, pk):
    question = Question.objects.get(id=pk)
    if request.method == 'POST':
        question.delete()
        return redirect('accounts:questions')
    context = {'question':question}
    return render(request, 'admin/questions.html', context)


@login_required
def groups(request):
    groups = Group.objects.all()
    context = {'groups': groups}
    return render(request, 'admin/groups.html', context)


@login_required
def group_page(request, id):
    group = Group.objects.get(id=id)
    userGroupForm = UserGroupForm()
    # users = CustomUser.objects.filter(groups__name=group)
    users = group.user_set.all()
    context = {'group': group,'userGroupForm': userGroupForm, 'users': users}
    return render(request, 'admin/single-group-page.html', context)


def group_add_user(request, id):
    group = Group.objects.get(id=id)
    add_user_to_group_form = UserGroupForm(request.POST)
    if add_user_to_group_form.is_valid():
        user = add_user_to_group_form.save(commit=False)
        user.usename = add_user_to_group_form.cleaned_data['username']
        print(user.username)
        user.groups.add(group)
    #user = 
    #group.user_set.add(user)
    context = {'group': group, 'add_user_to_group_form': add_user_to_group_form,}
    return render(request, 'admin/single-group-page.html', context) 


def answersPage(request):
    answers = Answer.objects.all().order_by('-add_time')
    #questions = Question.objects.annotate(total_answers=Count('answer__question')).order_by('-total_answers')
    paginator = Paginator(answers, 5)
    page_num = request.GET.get('page', 1)
    answers = paginator.page(page_num)
    context = {'answers': answers,}
    return render(request, 'admin/answers.html', context)


@login_required
def user_page(request, id):
    user = CustomUser.objects.get(id=id)
    userForm = UserEditForm()
    # users = CustomUser.objects.filter(groups__name=group)
    #users = group.user_set.all()
    context = {'user': user,'userForm': userForm,}
    return render(request, 'admin/user-page.html', context)


# Tags Page
def topics(request):
    topics=Topic.objects.all()
    context = {'topics':topics,}
    return render(request,'admin/topics.html', context)



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
    return render(request,'admin/topic.html',context)


# def deleteTopic(request, pk):
#     topic = Topic.objects.get(id=pk)
#     if request.method == 'POST':
#         topic.delete()
#         return redirect('accounts:topics')
#     context = {'topic':topic}
#     return render(request, 'admin/delete-topic.html', context)


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
    return render(request, 'admin/single-question-page.html', context)
