from main.models import Topic, Question, Answer
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .models import CustomUser
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from .forms import CreateUserForm, UserEditForm, UserLoginForm
from .token import account_activation_token
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import UserForm, ProfileForm
from django.contrib.auth.models import User
from .models import Profile
from accounts.decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.db.models import Count


from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from .forms import UserForm, ProfileForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from django.contrib.auth.models import Group
from django.core.paginator import Paginator





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
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your details have been updated successfully')
    else:
        user_form = UserEditForm(instance=request.user)
    context = {'user_form': user_form}
    return render(request,'registration/update_profile.html',context)


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
    context = {}
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
def delete_user(request, pk):
    user = CustomUser.objects.get(id=pk)
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