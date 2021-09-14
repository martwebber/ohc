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
    # path('profile/', ProfileView.as_view(), name='profile'),
    # path('profile/edit/', ProfileUpdateView.as_view(), name='edit'),
    # path('edit/', views.edit_profile, name='edit'),
    path('profile/edit/', views.edit, name='edit'),

     path('profile/', views.profile, name='profile'),
    # path('profile/edit/', views.edit_profile, name='edit'),
    # path('login/', auth_views.LoginView.as_view(template_name="registration/login.html",
    #                                             authentication_form=UserLoginForm), name='login'),
    path('login/', views.login, name='login'),
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

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/users', views.users, name='users'),
    path('admin-dashboard/users/<int:id>', views.user_page, name='user_page'),
    path('admin-dashboard/user/<int:id>', views.delete_user, name='delete_user'),
    path('admin-dashboard/questions/', views.questionsPage, name='questions'),
    path('admin-dashboard/answers/', views.answersPage, name='answers'),
    path('admin-dashboard/questions/<int:pk>', views.delete_question, name='delete_question'),
    path('admin-dashboard/groups/', views.groups, name='groups'),
    path('admin-dashboard/groups/<int:id>', views.group_page, name='group_page'),
    path('admin-dashboard/groups/<int:id>', views.group_add_user, name='group_add_user'),

    path('admin-dashboard/topics/',views.topics,name='topics'),
    path('admin-dashboard/topic/<int:pk>',views.topic,name='topic'),






]
