from rest_framework import serializers
from main import models

class NewProjectSerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    manager = serializers.HyperlinkedRelatedField(many=False,
        read_only=True,
        view_name='project-manager')

    class Meta:
        model = models.Project
        fields = ['id',
                  'developer',
                  'manager',
                  'name',
                  'short_description',
                  'long_description',
                  'salary',
                  'expectedDuration',
                  'status',
                  'creation_date',
                  'tags',]


class NewClientSerializer(serializers.HyperlinkedModelSerializer):
    projects = serializers.HyperlinkedRelatedField(many=True, view_name='project-detail', read_only=True)

    class Meta:
        model = models.Client
        fields = fields = (
      'id',
      'password',
      'username',
      'name',
      'surname',
      'university',
      'company',
      'biography',
      'email',
      'profil_picture',
      'date_joined',
      'last_login',
      'is_admin',
      'is_active',
      'is_staff',
      'is_superuser',
      'projects',
    )

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
    project = serializers.StringRelatedField(many=True, read_only=True)
    fields = (
      'id',
      'name',
      'project',
    )
    model = models.Tags

class RegistrationSerializer(serializers.ModelSerializer):

	password2	= serializers.CharField(style={'input_type': 'password'}, write_only=True)

	class Meta:
		model = models.Client
		fields = ['email', 'username', 'password', 'password2']
		extra_kwargs = {
				'password': {'write_only': True},
		}	

	def	save(self):

		account = models.Client(
					email=self.validated_data['email'],
					username=self.validated_data['username']
				)
		password = self.validated_data['password']
		password2 = self.validated_data['password2']
		if password != password2:
			raise serializers.ValidationError({'password': 'Passwords must match.'})
		account.set_password(password)
		account.save()
		return account

class ClientSerializer(serializers.ModelSerializer):
  token = serializers.ReadOnlyField(source = 'my_token')
  class Meta:
    fields = (
      'id',
      'token',
      'password',
      'username',
      'name',
      'surname',
      'university',
      'company',
      'biography',
      'email',
      'profil_picture',
      'date_joined',
      'last_login',
      'is_admin',
      'is_active',
      'is_staff',
      'is_superuser',
    )
    model = models.Client

class ChatSerializer(serializers.ModelSerializer):
  class Meta:
    messages = serializers.StringRelatedField(many=True)
    fields = (
      'id',
      'first_participant',
      'second_participant',
      'project',
      'messages',
    )
    model = models.Chat
    depth = 1

class MessageSerializer(serializers.ModelSerializer):
  class Meta:
    chat = serializers.StringRelatedField(many=True)
    fields = (
      'id',
      'body',
      'sender_id',
      'receiver_id',
      'is_read',
      'chat',
      'sentTime',
    )
    model = models.Message