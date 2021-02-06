import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from .models import Work, Contributor
from .serializers import WorkSerializer, ContributorSerializer


# initialize the APIClient app
client = Client()

class ContributorViewSetTest(TestCase):
    """Test for contributors endpoint"""

    def setUp(self):
        Contributor.objects.create(name='Jose Luis Ramos')
        Contributor.objects.create(name='Luis Jose Ramos')
        Contributor.objects.create(name='Jose Luis martinez')
        Contributor.objects.create(name='Luis Jose Martinez')


    def test_get_contributors(self):
        print('test_get_contributors')
        response = client.get('/contributors/')
        contributor_data = ContributorSerializer(Contributor.objects.all(), many=True).data
        self.assertEqual(response.data, contributor_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_retrieve_contributor(self):
        print('test_retrieve_contributor')
        instance = Contributor.objects.filter(name='Jose Luis Ramos').first()
        response = client.get('/contributors/' + str(instance.id) + '/')
        contributor_data = ContributorSerializer(instance).data
        self.assertEqual(response.data, contributor_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_retrieve_contributor_not_found(self):
        print('test_retrieve_contributor_not_exists')
        response = client.get('/contributors/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_post_contributor(self):
        print('test_post_contributor')
        CONTRIBUTOR_NAME = 'NEW'
        response = client.post('/contributors/',{'name': CONTRIBUTOR_NAME})
        contributor_data = ContributorSerializer(Contributor.objects.last()).data
        self.assertEqual(response.data, contributor_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_post_contributor_no_name(self):
        print('test_post_contributor_no_name')
        response = client.post('/contributors/',{'name': ''})
        self.assertContains(response, '"name":', status_code=400)


    def test_delete_contributor(self):
        print('test_delete_contributor')
        instance = Contributor.objects.last()
        response = client.delete('/contributors/' + str(instance.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_delete_contributor_not_found(self):
        print('test_delete_contributor_not_found')
        response = client.delete('/contributors/999.')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

