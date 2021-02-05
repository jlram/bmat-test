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

            # Skip the first line of the csv as it contains the headers
            reader.__next__()

            for row in reader:
                # Row values : 
                # [0]: name,
                # [1]: contributors,
                # [2]: iswc,
                # [3]: source,
                # [4]: id

                if row[2] == '': #iswc is empty
                    no_iswc.append(row)
                else:
                    work_qs = Work.objects.filter(iswc=row[2])

                    if not work_qs.exists():
                        work = Work.objects.create(
                            title=row[0],
                            iswc=row[2]
                        )
                    else:
                        work = work_qs.first()
                        check_title(work, row)

                ## Extract contributors and sources
                contributors = []
                sources = []
                
                for name in row[1].split('|'):
                    contributor = Contributor.objects.get_or_create(
                        name=name
                    )[0]

                    contributors.append(contributor)
                
                source = Source.objects.get_or_create(
                    name=row[3],
                    id_source=int(row[4])
                )[0]

                sources.append(source)
                
                
                work.contributors.add(*contributors)

                for source in sources:
                    source.work = work
                    source.save()

            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No file attached'}, status=status.HTTP_406_NOT_ACCEPTABLE)

def check_title(work, row):
    titles = work.title.split('|')

    title_exists = False
    for title in titles:
        if title == row[0]:
            title_exists = True

    if not title_exists:
        work.title += '|' + row[0]
        work.save()