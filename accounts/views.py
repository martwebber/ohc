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



from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import UserForm, ProfileForm
from django.contrib.auth.models import User
from .models import Profile

from django.contrib import messages


from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .forms import UserForm, ProfileForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect



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

