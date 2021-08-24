from main.models import Topic, Question, Answer
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .models import CustomUser
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import login
from django.contrib import messages
from .forms import CreateUserForm, UserEditForm
from .token import account_activation_token
from django.contrib.auth.decorators import login_required


# User Register
def register(request):
    if request.method == 'POST':
        registerForm = CreateUserForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
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
        login(request, user)
        return redirect('login')
    else:
        return render(request, 'registration/activation_invalid.html')


# Profile
def profile(request, id):
    user = CustomUser.objects.get(pk=id)
    questions=Question.objects.filter(user=request.user).order_by('-id')
    answers=Answer.objects.filter(user=request.user).order_by('-id')
    topics=Topic.objects.filter(user=request.user).order_by('-id')
    context = {'user':user, 'questions':questions, 'answers':answers, 'topics':topics}
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
