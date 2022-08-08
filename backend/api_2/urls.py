from django.urls import path
from . import views
from api.views import *
from api.views2 import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [

  #traverseable
  path('project/<int:pk>/manager', views.projectManager), #'GET'
  path('project/<int:pk>/developer', views.projectDeveloper), #'GET'
  path('client/<int:pk>/projects', views.clientProject), #'GET', 'POST'
  path('project/<int:pk>/tags', views.projectTag), #'GET','POST'
  path('client/<int:pk>/messages', views.clientMessage), #'GET','POST'
  path('chat/<int:pk>/messages', views.chatMessage), #'GET','POST'
  path('client/<int:pk>/chats', views.clientChat), #'GET','POST'

  #project
  path('projects/', views.projects), #'GET','POST'
  path('projectAll/<int:pk>', views.getAllProject), #'GET'
  path('project/<int:pk>', views.project, name = 'project-detail'), #'GET','PUT','DELETE'
  path('myproject/<int:pk>', views.getMyProject), #'GET'

  #client  
  path('clients/', views.clients), #'GET','POST'
  path('client/<int:pk>/', views.client), #'GET','PUT','DELETE'
  path('registration', views.registration_view),  #'POST'
  path('login', views.obtain_auth_token), #'POST'

  #tag
  path('tags/', views.tags), #'GET','POST'
  path('tag/<int:pk>/', views.tag), #'GET','PUT','DELETE'

  #chat
  path('mychats/<int:pk>/', views.getMyChats), #'GET'
  path('chats/', views.chats), #'GET','POST'
  path('chat/<int:pk>', views.chat), #'GET','PUT','DELETE'

  #message
  path('mymessages/<int:pk>/', views.getMyMessages), #'GET'
  path('messages/', views.customMessages),#'GET','POST'
  path('message/<int:pk>', views.messages), #'GET','PUT','DELETE'
]