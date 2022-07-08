from multiprocessing.connection import Client
from django.shortcuts import render
from django.views.generic.list import ListView
from main.models import *

# Create your views here.

class ProjectList(ListView):
  model = Project

