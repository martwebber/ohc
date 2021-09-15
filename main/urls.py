from django.urls import path
from . import views
from .views import UpdateQuestionView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns






app_name = 'main'


urlpatterns = [
    path('', views.home, name='home'),
    path('questions/', views.questionsPage, name='questions_page'),
    path('ask-question/', views.ask_question, name='ask_question'),
    path('question/<int:id>', views.single_question_page, name='single_question_page'),
    path('update-question/<int:id>', views.updateQuestion, name="update_question"),
    path('delete-question/<int:pk>', views.deleteQuestion, name="delete_question"),
    path('fav/<int:id>', views.favourite_add, name='favourite_add'),
    path('profile/favourites/', views.favourite_list, name='favourite_list'),
    path('delete-answer/<int:pk>', views.deleteAnswer, name="delete_answer"),
    path('update-answer/<int:pk>', views.updateAnswer, name="update_answer"),
    path('topic/<int:pk>',views.topic,name='topic'),

   # Tag Page
    path('tag/<str:tag>',views.tag,name='tag'),
    # Tags Page
    path('tags',views.tags,name='tags'),

    path('search/', views.question_search, name='question-search'),

    path('topic/<int:pk>/followers/add', views.followTopic, name='follow-topic'),

    path('topic/<int:pk>/followers/remove', views.unfollowTopic, name='unfollow-topic'),

    path('answer/<int:pk>/like', views.AddLike, name='like'),
    path('answer/<int:pk>/dislike', views.AddDislike, name='dislike'),

    path('topics/',views.topics,name='topics'),

    path('add-topic/', views.add_topic, name='add_topic'),

    





]


#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)