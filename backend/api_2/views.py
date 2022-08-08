import re
from django.test import RequestFactory
from requests import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from main.models import *
from api_2.serializers import *
from rest_framework import renderers
from rest_framework.request import Request
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema
from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.views import APIView


# Create your views here.

# Project -------------------------------------


# relations: Project -> Client (Manager)  DONE
#            Client (Manager) -> Project  DONE

#            Project -> Client (Developer)   DONE
#            Client (Developer) -> Project  DONE

#            Project -> Tags  DONE
#            Tags -> Project

#            Message -> Client
#            Client -> Message  DONE

#            Chat -> Message  DONE
#            Message -> Chat

#            Chat -> Client
#            Client -> Chat DONE


@api_view(['GET', 'POST'])
def projectDeveloper(request,pk):
  project = Project.objects.get(id = pk)
  client = Client.objects.get(id = project.developer)
  serializer = ClientSerializer(client, many = False)
  return Response(serializer.data)

@api_view(['GET', 'POST'])
def clientProject(request,pk):
  if request.method == 'GET':
    project = Project.objects.filter(manager = pk)
    project2 = Project.objects.filter(developer = pk)
    projects = project.union(project2)
    serializer = ProjectSerializer(projects)
    return Response(serializer.data)
  elif request.method == 'POST':
    data = request.data
    manager_instance = Client.objects.get(pk = pk)
    project = Project.objects.create(
      developer = data['developer'],
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
  else:
    return Response({'message': 'Enter a valid request'})


@api_view(['GET', 'POST'])
def projectManager(request, pk):
  project = Project.objects.get(id = pk)
  client = Client.objects.get(id = project.manager_id)
  serializer = ClientSerializer(client, many = False)
  return Response(serializer.data)

@api_view(['GET', 'POST'])
def projectTag(request, pk):
  if request.method == 'GET':
    tag = Tags.objects.filter(project = pk)
    serializer = TagSerializer(tag, many = True)
    return Response(serializer.data)
  elif request.method == 'POST':
    data  = request.data
    project_instance = Project.objects.get(id =pk)
    tag = Tags.objects.create(
      name=data['name'],
      project = project_instance,
    )
    serializer = TagSerializer(tag, many = False)
    return Response(serializer.data)
  else:
    return Response({'message': 'Enter a valid request'})
  
@api_view(['GET', 'POST'])
def clientMessage(request, pk):
  if request.method == 'GET':
    messages = Message.objects.filter(sender_id = pk)
    messages2 = Message.objects.filter(receiver_id = pk)
    message = messages2.union(messages) 
    serializer = MessageSerializer(message, many = True)
    return Response(serializer.data)
  elif request.method == 'POST':
    data  = request.data
    sender_instance = Client.objects.get(id = pk)
    receiver_instance = Client.objects.get(pk=data['receiver_id'])
    chat = Chat.objects.filter(first_participant = sender_instance, second_participant = receiver_instance)
    chat2 = Chat.objects.filter(first_participant = receiver_instance, second_participant = sender_instance)
    chat2 = chat2.union(chat)
    message = Message.objects.create(
      body=data['body'],
      sender_id = sender_instance,
      receiver_id = receiver_instance,
      is_read=data['is_read'],
      chat = chat2.first(),
    )
    serializer = MessageSerializer(message, many = False)
    return Response(serializer.data)
  else:
    return Response({'message': 'Enter a valid request'})

@api_view(['GET', 'POST'])
def chatMessage(request,pk):
  if request.method == 'GET':
    messages = Message.objects.filter(chat_id = pk)
    serializer = MessageSerializer(messages, many = True)
    return Response(serializer.data)
  elif request.method == 'POST':
    data  = request.data
    sender_instance = Client.objects.get(pk=data['sender_id'])
    receiver_instance = Client.objects.get(pk=data['receiver_id'])
    chat_instance = Chat.objects.get(id=pk)

    message = Message.objects.create(
      body=data['body'],
      sender_id = sender_instance,
      receiver_id = receiver_instance,
      is_read=data['is_read'],
      chat = chat_instance,
    )
    serializer = MessageSerializer(message, many = False)
    return Response(serializer.data)
  else:
    return Response({'message': 'Enter a valid request'})

@api_view(['GET', 'POST'])
def clientChat(request, pk):
  if request.method == 'GET':
    chat = Chat.objects.filter(first_participant = pk)
    chat2 = Chat.objects.filter(second_participant = pk)
    chats = chat.union(chat2)
    serializer = ChatSerializer(chats, many = True)
    return Response(serializer.data)
  elif request.method == 'POST':
    data  = request.data
    first_p_instance = Client.objects.get(pk=pk)
    second_p_instance = Client.objects.get(pk=data['second_participant'])
    project_instance = Project.objects.get(pk=data['project'])

    chat = Chat.objects.create(
      first_participant = first_p_instance,
      second_participant = second_p_instance,
      project = project_instance,
    )
    serializer = ChatSerializer(chat, many = False)
    return Response(serializer.data)
  else:
    return Response({'message': 'Enter a valid request'})

@api_view(['GET', 'POST'])
def projects(request):
  
  factory = RequestFactory()
  request = factory.get('/')


  serializer_context = {
      'request': Request(request),
  }

  if request.method == 'GET':
    projects = Project.objects.all()
    serializer = NewProjectSerializer(projects, context=serializer_context, many = True)
    return Response(serializer.data)
  elif request.method == 'POST':
    data  = request.data
    developer_instance = None
    #if(data['developer']!=None):
    #  developer_instance = Client.objects.get(pk = data['developer'])
    manager_instance = Client.objects.get(pk = data['manager'])
    project = Project.objects.create(
      #developer = developer_instance,
      developer = data['developer'],
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

@api_view(['GET'])
def getAllProject(request, pk):
  project = Project.objects.filter(status = "PENDING").exclude(manager = pk)
  serializer = ProjectSerializer(project, many = True)
  return Response(serializer.data)

@api_view(['GET'])
# @permission_classes((IsAuthenticated,))
def getMyProject(request, pk):
  projectManager = Project.objects.filter(manager = pk)
  projectDeveloper = Project.objects.filter(developer = pk)
  projectDeveloper = projectDeveloper.union(projectManager)
  serializer = ProjectSerializer(projectDeveloper, many = True)
  return Response(serializer.data) #, {'response':"You don't have permission to edit that."})


# Client --------------------------------


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
  user = request.user
  if request.method == 'GET':
    serializer = ClientSerializer(client, many = False)
    return Response(serializer.data)
  elif request.method == 'PUT':
    serializer = ClientSerializer(client, data=request.data, partial=True)
    if client != user:
          return Response({'response':"You don't have permission to edit that."})
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
  elif request.method == 'DELETE':
    client.delete()
    return Response({'message': 'Client was deleted successfully!'})
  else:
    return Response({'message': 'Enter a valid request'})

@api_view(['POST', ])
def registration_view(request):

	if request.method == 'POST':
		serializer = RegistrationSerializer(data=request.data)
		data = {}
		if serializer.is_valid():
			account = serializer.save()
			data['response'] = 'successfully registered new user.'
			data['userid'] = account.id #previously was email
			data['username'] = account.username
			token = Token.objects.get(user=account).key
			data['token'] = token
      # data['userid'] = account.id
		else:
			data = serializer.errors
		return Response(data)


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    if coreapi_schema.is_enabled():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="username",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Username",
                        description="Valid username for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'userid': user.id})


obtain_auth_token = ObtainAuthToken.as_view()

# Tag ---------------------------


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
    return Response({'message': 'Tutorial was deleted successfully!'})
  else:
    return Response({'message': 'Enter a valid request'})


# Chat ----------------------------


@api_view(['GET'])
def getMyChats(request, pk):
  chats = Chat.objects.filter(first_participant = pk)
  chats2 = Chat.objects.filter(second_participant = pk)
  chats2 = chats2.union(chats)
  serializer = ChatSerializer(chats2, many = True)
  return Response(serializer.data)

@api_view(['GET', 'POST'])
def chats(request):
  if request.method == 'GET':
    chats = Chat.objects.all()
    serializer = ChatSerializer(chats, many = True)
    return Response(serializer.data)
  elif request.method == 'POST':
    data  = request.data
    first_p_instance = Client.objects.get(pk=data['first_participant'])
    second_p_instance = Client.objects.get(pk=['second_participant'])
    project_instance = Project.objects.get(pk=data['project'])

    chat = Chat.objects.create(
      first_participant = first_p_instance,
      second_participant = second_p_instance,
      project = project_instance,
    )
    serializer = ChatSerializer(chat, many = False)
    return Response(serializer.data)
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


# Message -----------------------


@api_view(['GET', 'POST'])
def customMessages(request):
  if request.method == 'GET':
    messages = Message.objects.all()
    serializer = MessageSerializer(messages, many = True)
    return Response(serializer.data)
  elif request.method == 'POST':
    data  = request.data
    sender_instance = Client.objects.get(pk=data['sender_id'])
    receiver_instance = Client.objects.get(pk=data['receiver_id'])
    chat_instance = Chat.objects.get(pk=data['chat'])

    message = Message.objects.create(
      body=data['body'],
      sender_id = sender_instance,
      receiver_id = receiver_instance,
      is_read=data['is_read'],
      chat = chat_instance,
    )
    serializer = MessageSerializer(message, many = False)
    return Response(serializer.data)
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
    message.delete()
    return Response({'message': 'Message was deleted successfully!'})
  else:
    return Response({'message': 'Enter a valid request'})

@api_view(['GET'])
def getMyMessages(request, pk):
  messages = Message.objects.filter(chat_id = pk)
  serializer = MessageSerializer(messages, many = True)
  return Response(serializer.data)
