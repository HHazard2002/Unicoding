from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from main.models import *

class AccountTests(APITestCase):

    url = "/api/v1/project2/"
    url2 = "/api/v1/client2/"

    def setUp(self):
        Project.objects.create(name = "project",short_description = "another test",long_description =  "dsfdsf", 
        salary = 200, expectedDuration = "6 Months", status = "PENDING", creation_date = "2022-03-23T01:29:56.581084Z")

        Client.objects.create(name = "Henry", surname = "Hurst", university = "UoB", company = "n/a",
        biography = "sdfsd", emailAddress = "henry@gmail.com")
    
    def test_create_project(self):   

        response = self.client.get(self.url)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["name"], 'project')

    def test_post_project(self):
      data = {"name": "project 2", "short_description": "another test", "long_description": "dsfdsf",
        "salary": 200, "expectedDuration": "6 Months", "status": "PENDING", "creation_date": "2022-03-23T01:29:56.581084Z"}

      response = self.client.post(self.url, data = data)
      result = response.json()

      self.assertEqual(response.status_code, 201)
      #self.assertEqual(result["name"], "project 2")


    def test_update_project(self):
      pk = "1"
      data = { "name": "Modified test"}

      response = self.client.patch(self.url + f"{pk}/", data=data)
      result = response.json()

      self.assertEqual(response.status_code, 405)
      #self.assertEqual(result["name"], "project 2")

#--------------------------------------------------------------------------------

    def test_create_client(self):   

        response = self.client.get(self.url2)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["name"], 'Henry')

    def test_post_client(self):
      data = { "name": "Henry2", "surname": "Hurst", "university": "UoB", "company": "n/a", "biography": "sdfsd",
        "emailAddress": "henry@gmail.com"}

      response = self.client.post(self.url2, data = data)
      result = response.json()

      self.assertEqual(response.status_code, 201)
      self.assertEqual(result["name"], "Henry2")


    def test_update_client(self):
      pk = "1"
      data = { "name": "Hugo"}

      response = self.client.patch(self.url2 + f"{pk}/", data=data)
      result = response.json()

      self.assertEqual(response.status_code, 405)
      #self.assertEqual(result["name"], "Hugo")