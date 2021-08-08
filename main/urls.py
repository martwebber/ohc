from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('ask-question/', views.ask_question, name='ask_question'),
    path('create-post/', views.create_post, name='create_post'),
    path('question/<int:id>', views.single_question_page, name='single_question_page'),
    path('save-comment', views.save_comment, name='save-comment'),
    # path('save-comment2',views.save_comment2,name='save-comment2'),
    path('delete-question/<int:pk>', views.deleteQuestion, name="delete_question"),
    path('update_question/<int:pk>', views.update_question, name="update_question"),
    path('posts/', views.posts_page, name='posts_page'),




]
