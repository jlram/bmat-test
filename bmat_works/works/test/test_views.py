import os
from bmat_works.settings import BASE_DIR
from rest_framework import status
from django.test import TestCase, Client
from ..models import Work, Source, Contributor


# initialize the APIClient app
client = Client()

class ImportCSVViewSetTest(TestCase):
    """Test for CSV Import"""

    data = None

    def setUp(self):
        file_path = os.path.join(BASE_DIR, 'works_metadata.csv')
        self.data = open(file_path, 'r')

    def test_import_csv_no_file(self):
        print('test_import_csv_no_file')
        response = client.post('/import_csv/')
        self.assertContains(response, '"error":', status_code=406)

    def test_import_csv(self):
        print('test_import_csv')
        response = client.post('/import_csv/', {'file': self.data})
        work_count = Work.objects.all().count()
        self.assertEqual(work_count, 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ExportCSVViewSetTest(TestCase):
    """Test for CSV Export"""

    def setUp():
        show_me_how = Work.objects.create(
            title='Show Me How',
            iswc='TS1234568'
        )

        show_me_how.contributors.set([
            Contributor.objects.create(name='Emmanuelle Proulx'),
            Contributor.objects.create(name='Jessy Caron'),
            Contributor.objects.create(name='Dragos Chiriac')
        ])