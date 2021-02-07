import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from .models import Work, Contributor, Source
from .serializers import WorkSerializer, ContributorSerializer, SourceSerializer


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
        print('test_retrieve_contributor_not_found')
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


class SourceViewSetTest(TestCase):
    """Test for contributors endpoint"""

    def setUp(self):
        Source.objects.create(name='Sony', id_source=1)
        Source.objects.create(name='Warner', id_source=1)
        Source.objects.create(name='Universal', id_source=1)


    def test_get_sources(self):
        print('test_get_sources')
        response = client.get('/sources/')
        source_data = SourceSerializer(Source.objects.all(), many=True).data
        self.assertEqual(response.data, source_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_retrieve_contributor(self):
        print('test_retrieve_source')
        instance = Source.objects.filter(name='Sony').first()
        response = client.get('/sources/' + str(instance.id) + '/')
        source_data = SourceSerializer(instance).data
        self.assertEqual(response.data, source_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_retrieve_source_not_found(self):
        print('test_retrieve_source_not_found')
        response = client.get('/sources/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_post_source(self):
        print('test_post_source')
        SOURCE_NAME = 'NEW'
        response = client.post('/sources/',{'name': SOURCE_NAME, 'id_source': 1})
        source_data = SourceSerializer(Source.objects.last()).data
        self.assertEqual(response.data, source_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_post_source_no_data(self):
        print('test_post_source_no_data')
        response = client.post('/sources/',{})
        self.assertContains(response, '"name":', status_code=400)


    def test_delete_source(self):
        print('test_delete_source')
        instance = Source.objects.last()
        response = client.delete('/sources/' + str(instance.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_delete_source_not_found(self):
        print('test_delete_source_not_found')
        response = client.delete('/sources/999.')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


