from django.urls import path
from . import views
from api.views import ListChats, DetailChat, ListClients, DetailClient, ListMessages, DetailMessage, ListTags, DetailTag, ListProjects, DetailProject

urlpatterns = [
  #project
  path('project2/', ListProjects.as_view()),
  path('project2/<int:pk>/', DetailProject.as_view()),

  path('project/', views.getProjects),
  path('project/<int:pk>/', views.getProject),
  path('project/create', views.createProject),
  path('projectAll/<int:pk>', views.getAllProject),
  path('myproject/<int:pk>', views.getMyProject),
  path('project/<int:pk>/delete', views.deleteProject),

  #client
  path('client2/', ListClients.as_view()),
  path('client2/<int:pk>/', DetailClient.as_view()),

  path('client/', views.getClients),
  path('client/<int:pk>/', views.getClient),
  path('client/create', views.createClient),
  path('client/<int:pk>/delete', views.deleteClient),
  #tag
  path('tag/', views.getTags),
  path('tag/<int:pk>/', views.getTag),
  path('tag/create', views.createTag),
  path('tag/<int:pk>/delete', views.deleteTag),

  path('tag2/', ListTags.as_view()),
  path('tag2/<int:pk>/', DetailTag.as_view()),
  #chat
  path('chat/', ListChats.as_view()),
  path('chat/<int:pk>/', DetailChat.as_view()),
  #message
  path('message/', ListMessages.as_view()),
  path('message/<int:pk>/', DetailMessage.as_view()),
]