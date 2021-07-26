from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('ask-question/', views.ask_question, name='ask_question'),
    path('question/', views.answer, name='answer'),
]
