from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('ask-question/', views.ask_question, name='ask_question'),
    path('question/<int:id>', views.single_question_page, name='single_question_page'),
    path('save-comment', views.save_comment, name='save-comment'),
    # path('save-comment2',views.save_comment2,name='save-comment2'),

]
