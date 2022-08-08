from email import message
from email.policy import default
from unicodedata import name
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.dispatch import receiver

# Create your models here.

class Client(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
  name = models.CharField(max_length = 60, default="")
  surname = models.CharField(max_length=60, default=" ")
  university = models.CharField(max_length=60, default="")
  company = models.CharField(max_length=60, default="")
  biography = models.TextField(max_length=750, default="")
  emailAddress = models.EmailField(default="")

  def __str__(self):
    return self.name



class Project(models.Model):

  STATUS_CHOICES = (("PENDING", 'Pending'), ("ON GOING", 'On going'), ("FINISHED", 'Finished'))

  developer = models.ForeignKey(Client, on_delete=models.CASCADE, related_name = 'developing_project', blank = True, null = True)
  manager = models.ForeignKey(Client, on_delete=models.CASCADE, related_name = 'managed_project', blank = True, null = True)
  # developer = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'developing_project', blank = True, null = True)
  # manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'managed_project', blank = True, null = True)
  name = models.CharField(max_length= 100)
  short_description = models.CharField(max_length=150)
  long_description = models.CharField(max_length= 750)
  salary = models.IntegerField()
  expectedDuration = models.CharField(max_length=20, default = "1 day")
  status = models.CharField(max_length = 8, choices = STATUS_CHOICES, default = "PENDING")
  creation_date = models.DateTimeField(auto_now_add = True)


  def __str__(self):
      return self.name

class Tags(models.Model):
  name = models.CharField(max_length=20)
  project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tags', blank = True, null = True)
  
  def __str__(self):
    return self.name
    
class Message(models.Model):
  body = models.TextField()
  sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_sender', blank = True, null = True)
  receiver_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_recepient', blank = True, null = True)
  sentTime = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.body
  
class Chat(models.Model):
  participants = models.ManyToManyField(User, blank = True, null = True)
  messages = models.ManyToManyField(Message, blank=True, null=True)

  def __str__(self):
    return "{}".format(self.pk)

