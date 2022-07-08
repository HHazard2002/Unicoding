from asyncio.base_futures import _PENDING
from contextlib import nullcontext
from email import message
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from main.models import *
from api.serializers import *

# Create your views here.

# Clients -------------------------------------------------------------------------------------------------

@api_view(['GET', 'POST'])
def clients (request):
  if request.method == 'GET':
    clients = Client.objects.all()
    serializer = ClientSerializer(clients, many = True)
    return Response(serializer.data)
  elif request.method == 'POST':
    data  = request.data
    client = Client.objects.create(
      password=data['password'],
      username=data['username'],
      name=data['name'],
      surname =data['surname'],
      university = data['university'],
      company = data['company'],
      biography = data['biography'],
      email = data['email'],
    )
    serializer = ClientSerializer(client, many = False)
    return Response(serializer.data)
  else:
    return Response({'message': 'Enter a valid request'})

@api_view(['GET', 'PUT', 'DELETE'])
def client(request, pk):
  client = Client.objects.get(id = pk)
  if request.method == 'GET':
    serializer = ClientSerializer(client, many = False)
    return Response(serializer.data)
  elif request.method == 'PUT':
    serializer = ClientSerializer(client, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
  elif request.method == 'DELETE':
    client.delete()
    return Response({'message': 'Client was deleted successfully!'})
  else:
    return Response({'message': 'Enter a valid request'})

@api_view(['GET', 'PUT', 'DELETE'])
def project(request, pk):
  project = Project.objects.get(id = pk)
  user = request.user
  if request.method == 'GET':
    serializer = ProjectSerializer(project, many = False)
    return Response(serializer.data)
  elif request.method == 'PUT':
    serializer = ProjectSerializer(project, data=request.data, partial=True)
    if project.manager != user:
          return Response({'response':"You don't have permission to edit that."})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
  elif request.method == 'DELETE':
    if project.manager != user:
        return Response({'response':"You don't have permission to edit that."})
    project.delete()
    return Response({'message': 'Project was deleted successfully!'})
  else:
    return Response({'message': 'Enter a valid request'})


@api_view(['GET', 'POST'])
def tags(request):
  if request.method == 'GET':
    tags = Tags.objects.all()
    serializer = TagSerializer(tags, many = True)
    return Response(serializer.data)
  elif request.methods == 'PUT':
    data  = request.data
    project_instance = Project.objects.get(pk=data['project'])
    tag = Tags.objects.create(
      name=data['name'],
      project = project_instance,
    )
    serializer = TagSerializer(tag, many = False)
    return Response(serializer.data)
  else:
    return Response({'message': 'Enter a valid request'})

@api_view(['GET', 'PUT', 'DELETE'])
def tag(request, pk):
  tag = Tags.objects.get(id = pk)
  if request.method == 'GET':
    serializer = TagSerializer(tag, many = False)
    return Response(serializer.data)
  elif request.method == 'PUT':
    serializer = TagSerializer(tag, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
  elif request.method == 'DELETE':
    tag.delete()
    return Response({'message': 'Tag was deleted successfully!'})
  else:
    return Response({'message': 'Enter a valid request'})


@api_view(['GET', 'PUT', 'DELETE'])
def chat(request, pk):
  chat = Chat.objects.get(id = pk)
  if request.method == 'GET':
    serializer = ChatSerializer(chat, many = False)
    return Response(serializer.data)
  elif request.method == 'PUT':
    serializer = ChatSerializer(chat, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
  elif request.method == 'DELETE':
    chat.delete()
    return Response({'message': 'Chat was deleted successfully!'})
  else:
    return Response({'message': 'Enter a valid request'})

@api_view(['GET', 'PUT', 'DELETE'])
def messages(request, pk):
  message = Message.objects.get(id = pk)
  if request.method == 'GET':
    serializer = MessageSerializer(message, many = False)
    return Response(serializer.data)
  elif request.method == 'PUT':
    serializer = MessageSerializer(message, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
  elif request.method == 'DELETE':
    chat.delete()
    return Response({'message': 'Message was deleted successfully!'})
  else:
    return Response({'message': 'Enter a valid request'})
