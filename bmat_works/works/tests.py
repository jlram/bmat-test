import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from .models import Work, Contributor
from .serializers import WorkSerializer, ContributorSerializer


# initialize the APIClient app
client = Client()

class GetContributorsTest(TestCase):
    """Test for GET contributors"""

    def setUp(self):
        Contributor.objects.create(name='Jose Luis Ramos')
        Contributor.objects.create(name='Luis Jose Ramos')
        Contributor.objects.create(name='Jose Luis martinez')
        Contributor.objects.create(name='Luis Jose Martinez')
    
    def test_get_contributors(self):
        response = client.get(reverse('contributor-list'))
        contributor_data = ContributorSerializer(Contributor.objects.all(), many=True).data
        self.assertEqual(response.data, contributor_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
