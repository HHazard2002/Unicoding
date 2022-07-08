from asyncio.base_futures import _PENDING
from contextlib import nullcontext
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from main.models import *
from api.serializers import *

# Create your views here.

# Project -------------------------------------------------------------------------------------------------
class ListProjects(generics.ListCreateAPIView):
  queryset = models.Project.objects.all()
  serializer_class = ProjectSerializer

class DetailProject(generics.RetrieveDestroyAPIView):
  queryset = models.Project.objects.all()
  serializer_class = ProjectSerializer

@api_view(['GET'])
def getProjects(request):
  projects = Project.objects.all()
  serializer = ProjectSerializer(projects, many = True)
  return Response(serializer.data)

@api_view(['GET'])
def getProject(request, pk):
  project = Project.objects.get(id = pk)
  serializer = ProjectSerializer(project, many = False)
  return Response(serializer.data)

@api_view(['GET'])
def getAllProject(request, pk):
  project = Project.objects.filter(status = "PENDING").exclude(manager = pk)
  serializer = ProjectSerializer(project, many = True)
  return Response(serializer.data)

@api_view(['GET'])
def getMyProject(request, pk):
  projectManager = Project.objects.filter(manager = pk)
  projectDeveloper = Project.objects.filter(developer = pk)
  projectDeveloper = projectDeveloper.union(projectManager)
  serializer = ProjectSerializer(projectDeveloper, many = True)
  return Response(serializer.data)


@api_view(['POST'])
def createProject(request):
  data  = request.data
  # developer_instance = User.objects.get(pk = data['developer'])
  # manager_instance = User.objects.get(pk = data['manager'])
  developer_instance = None
  if(data['developer']!=None):
    developer_instance = Client.objects.get(pk = data['developer'])
  
  manager_instance = Client.objects.get(pk = data['manager'])

  project = Project.objects.create(
    developer = developer_instance,
    manager = manager_instance,
    name=data['name'],
    short_description=data['short_description'],
    long_description=data['long_description'],
    salary=data['salary'],
    expectedDuration=data['expectedDuration'],
    status=data['status'],
  )
  serializer = ProjectSerializer(project, many = False)
  return Response(serializer.data)

@api_view(['DELETE'])
def deleteProject(request, pk):
  project = Project.objects.get(id = pk)
  project.delete()
  return Response({'message': 'Project was deleted successfully!'})

# Client --------------------------------------------------------------------------------------------------
class ListClients(generics.ListCreateAPIView):
  queryset = models.Client.objects.all()
  serializer_class = ClientSerializer

class DetailClient(generics.RetrieveDestroyAPIView):
  queryset = models.Client.objects.all()
  serializer_class = ClientSerializer

@api_view(['GET'])
def getClients(request):
  clients = Client.objects.all()
  serializer = ClientSerializer(clients, many = True)
  return Response(serializer.data)

@api_view(['GET'])
def getClient(request, pk):
  client = Client.objects.get(id = pk)
  serializer = ClientSerializer(client, many = False)
  return Response(serializer.data)

@api_view(['POST'])
def createClient(request):
  data  = request.data

  client = Client.objects.create(
    user=data['user'],
    name=data['name'],
    surname =data['surname'],
    developer = data['developer'],
    university = data['university'],
    company = data['company'],
    biography = data['biography'],
    emailAddress = data['emailAddress'],
  )
  serializer = ClientSerializer(client, many = False)
  return Response(serializer.data)

@api_view(['DELETE'])
def deleteClient(request, pk):
  client = Client.objects.get(id = pk)
  client.delete()
  return Response({'message': 'Tutorial was deleted successfully!'})


# Tags ----------------------------------------------------------------------------------------------------
class ListTags(generics.ListCreateAPIView):
  queryset = models.Tags.objects.all()
  serializer_class = TagSerializer

class DetailTag(generics.RetrieveDestroyAPIView):
  queryset = models.Tags.objects.all()
  serializer_class = TagSerializer

@api_view(['GET'])
def getTags(request):
  tags = Tags.objects.all()
  serializer = TagSerializer(tags, many = True)
  return Response(serializer.data)

@api_view(['GET'])
def getTag(request, pk):
  tags = Tags.objects.get(id = pk)
  serializer = TagSerializer(tags, many = False)
  return Response(serializer.data)

@api_view(['POST'])
def createTag(request):
  data  = request.data
  project_instance = Project.objects.get(pk=data['project'])

  tag = Tags.objects.create(
    name =data['name'],
    project = project_instance,
  )
  serializer = TagSerializer(tag, many = False)
  return Response(serializer.data)

@api_view(['DELETE'])
def deleteTag(request, pk):
  tag = Tags.objects.get(id = pk)
  tag.delete()
  return Response({'message': 'Tutorial was deleted successfully!'})

# Chat ----------------------------------------------------------------------------------------------------
class ListChats(generics.ListCreateAPIView):
  queryset = models.Chat.objects.all()
  serializer_class = ChatSerializer

class DetailChat(generics.RetrieveDestroyAPIView):
  queryset = models.Chat.objects.all()
  serializer_class = ChatSerializer


# Message -------------------------------------------------------------------------------------------------
class ListMessages(generics.ListCreateAPIView):
  queryset = models.Message.objects.all()
  serializer_class = MessageSerializer

class DetailMessage(generics.RetrieveDestroyAPIView):
  queryset = models.Message.objects.all()
  serializer_class = MessageSerializer