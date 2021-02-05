import csv
import io

from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Work, Contributor, Source
from .serializers import WorkSerializer, ContributorSerializer, SourceSerializer

class WorkViewSet(viewsets.ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer


class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class ImportCSVViewSet(viewsets.ViewSet):
    
    def create(self, request):
        if 'file' in request.data:
            file = request.data['file']
            data_set = file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            reader = csv.reader(io_string)

            # Backup array for those songs with no iswc
            no_iswc = []

            # Skip the first line of the csv as it contains the titles
            reader.__next__()

            for row in reader:
                print(row)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No file attached'}, status=status.HTTP_406_NOT_ACCEPTABLE)