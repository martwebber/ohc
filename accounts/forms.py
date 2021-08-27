from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from .models import CustomUser, Profile


# Creating a Custom user registration form
class CreateUserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control mb-3',
            'placeholder': 'Username'
            })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control mb-3',
            'placeholder': 'Email',
            'name': 'email',
            'id': 'id_email'
            })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control mb-3',
            'placeholder': 'Password'
            })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control mb-3',
            'placeholder': 'Confirm Password'
            })

    username = forms.CharField(
        label='Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email')

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = CustomUser.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'The email address you entered is already taken. Please enter a different one.')
        return email


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Username',
                'id': 'login-username'
                }))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'id': 'login-pwd'
                }))


class PwordResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Email',
            'id': 'form-email'
            }))

    def clean_email(self):
        email = self.cleaned_data['email']
        test = CustomUser.objects.filter(email=email)
        if not test:
            raise forms.ValidationError(
                'The email address you have provided cannot be found. Try a different email address.')
        return email


class PwordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'New Password',
                'id': 'form-newpass'
                }))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'New Password',
                'id': 'form-new-pass2'
                }))


class PwordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Old Password', widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Old Password',
                'id': 'form-oldpass'
                }))
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'New Password',
                'id': 'form-newpass'
                }))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'New Password',
                'id': 'form-new-pass2'
                }))


class ProfileForm(ModelForm):
    class Meta:
        model=CustomUser
        fields=('first_name','last_name','username','bio','email')


class UserEditForm(forms.ModelForm):
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bio'].required = False
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['username'].required = True
        self.fields['email'].required = True

 
 
    bio = forms.CharField(
        label='Bio', min_length=10, max_length=100, widget=forms.Textarea(
            attrs={'rows':3, 'class': 'form-control mb-3', 'placeholder': 'Enter your bio', 'id': 'form-bio'}))
 
    first_name = forms.CharField(
        label='First Name', max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'First Name', 'id': 'form-firstname'}))
 
    last_name = forms.CharField(
        label='Last Name', max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Last Name', 'id': 'form-lastname'}))
 
    username = forms.CharField(
        label='Username', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-username'}))

    email = forms.EmailField(
        label='Email', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))
 
    class Meta:
        model = CustomUser
        fields = ('bio', 'first_name', 'last_name', 'email')
 
    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
        ]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'bio',
            'phone_number',
            'birth_date',
            'profile_image'
        ]