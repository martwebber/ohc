from django.urls import path
from . import views
# from django.contrib.auth.decorators import user_passes_test
# from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm, PwordResetForm, PwordResetConfirmForm, PwordChangeForm
from .views import ProfileUpdateView, ProfileView
app_name = 'accounts'


urlpatterns = [
    path('register/', views.register, name='register'),
    # Profile
    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit/', ProfileUpdateView.as_view(), name='edit'),
    # path('profile/<int:id>', views.profile, name='profile'),
    # path('profile/edit/', views.edit_profile, name='edit'),
    path('login/', auth_views.LoginView.as_view(template_name="registration/login.html",
                                                authentication_form=UserLoginForm), name='login'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name="registration/password_change_form.html", form_class=PwordChangeForm), name='password_change'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset_form.html", form_class=PwordResetForm), name='pwdreset'),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html', form_class=PwordResetConfirmForm), name="pwdresetconfirm"),
    # #path('/logout', auth_views.logout_then_login, name='logout'),
    # path('logout/', views.logout, name="logout"),
    # path('login/', views.login, name="login"),

    path('activate/<slug:uidb64>/<slug:token>)/', views.activate, name='activate'),
]
