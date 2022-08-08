from rest_framework import serializers
from main import models

class ProjectSerializer(serializers.ModelSerializer):
  class Meta:
    tags = serializers.StringRelatedField(many=True)
    fields = (
      'id',
      'developer',
      'manager',
      'name',
      'short_description',
      'long_description',
      'salary',
      'expectedDuration',
      'status',
      'creation_date',
      'tags',
    )
    model = models.Project
    depth = 1

class TagSerializer(serializers.ModelSerializer):
  class Meta:
    project = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    fields = (
      'id',
      'name',
      'project',
    )
    model = models.Tags

class ClientSerializer(serializers.ModelSerializer):
  class Meta:
    fields = (
      'id',
      'user',
      'name',
      'surname',
      'university',
      'company',
      'biography',
      'emailAddress',
    )
    model = models.Client

class ChatSerializer(serializers.ModelSerializer):
  class Meta:
    fields = (
      'id',
      'participants',
      'messages',
    )
    model = models.Chat

class MessageSerializer(serializers.ModelSerializer):
  class Meta:
    fields = (
      'id',
      'body',
      'sender_id',
      'receiver_id',
      'sentTime',
    )
    model = models.Message