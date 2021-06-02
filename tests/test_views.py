from django.test import TestCase, Client
from django.models import YoutubeChannel,YoutubeVideo
import json


class TestViews(TestCase):
	
	def setUp(self):
	self.client = client()
	self.list_url = reverse('list')



	def test_project_list_GET(self):
		client = client.get()
		response = client.get(reverse('list')
		
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, ListAPIView)
