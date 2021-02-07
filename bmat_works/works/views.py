import csv
import io

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Work, Contributor, Source
from .serializers import WorkSerializer, ContributorSerializer, SourceSerializer
from .utils import check_title, add_relations

class WorkViewSet(viewsets.ModelViewSet):
    """Work CRUD"""
    queryset = Work.objects.all()
    serializer_class = WorkSerializer

    def retrieve(self, request, pk=None):
        """RETRIEVE Work by ISWC instead of ID"""
        work = get_object_or_404(self.queryset, iswc=pk)
        serializer = WorkSerializer(work)
        return Response(serializer.data)


    def update(self, request, *args, **kwargs):
        """POST Work by ISWC instead of ID"""
        instance = self.queryset.get(iswc=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """DELETE Work by ISWC instead of ID"""
        work = get_object_or_404(self.queryset, iswc=pk)
        work.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ContributorViewSet(viewsets.ModelViewSet):
    """Contributor CRUD"""
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

    def update(self, request, *args, **kwargs):
        """Overridden ModelViewSet's PUT for Contributor, allowing partial update"""
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class SourceViewSet(viewsets.ModelViewSet):
    """Source CRUD"""
    queryset = Source.objects.all()
    serializer_class = SourceSerializer

    def update(self, request, *args, **kwargs):
        """Overridden ModelViewSet's PUT for Source, allowing partial update"""
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ImportCSVViewSet(viewsets.ViewSet):
    """
        :param `file`: .csv file
        :method POST
        :returns 200 OK
        :raises 406 NOT ACCEPTABLE

        Reads a csv file. Creates or completes information based on its content.

    """

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

                if row[2] == '':  # iswc is empty
                    no_iswc.append(row)
                else:
                    # Checks if Work with that iswc already exists
                    work_qs = Work.objects.filter(iswc=row[2])

                    if not work_qs.exists():
                        work = Work.objects.create(
                            title=row[0],
                            iswc=row[2]
                        )
                    else:
                        work = work_qs.first()
                        check_title(work, row[0])

                    # Adds contributors and sources to work
                    add_relations(work, row[1], (row[3], row[4]))

                    # Finally, checks songs with no iswc
                    # If they have the exact same title and contributors, we can consider
                    # both as the same track, even if the iswc is not present.
                    # If there are differences, we are risking to be mixing up two different songs.
                    for no_iswc_work in no_iswc:
                        filter = Q()  # Empty filter
                        
                        # For each contributor, adds a filter based on its name
                        for contributor in no_iswc_work[1].split('|'):
                            filter |= Q(name=contributor)
                        
                        contributor_qs = Contributor.objects.filter(filter)
                        work_qs = Work.objects.all()

                        for work in work_qs:
                            # Compare titles and then Querysets by turning them into sets
                            if no_iswc_work[0] in work.title.split('|') and set(work.contributors.all()) == set(Contributor.objects.filter(filter)):
                                add_relations(work, None, (no_iswc_work[3], no_iswc_work[4]))

            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No file attached'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class ExportCSVViewSet(viewsets.ViewSet):
    """
        Export Works, Contributors and Sources to a readable csv file
        :method GET
        :returns 200 OK
        :raises 204 NO CONTENT
    """

    def list(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="jlram_metadata.csv"'

        fieldnames = ['title', 'contributors', 'iswc', 'source', 'id']
        writer = csv.DictWriter(response, fieldnames)
        writer.writeheader()
        if Work.objects.all().count() > 0:
            for work in Work.objects.all():
                # Writes Contributor string, separated by |
                write_contributors = ''
                for index, contributor in enumerate(work.contributors.all()):
                    write_contributors += contributor.name + ('|' if index != len(work.contributors.all())-1 else '')

                # Writes Source string, separated by |
                sources = Source.objects.filter(work=work)
                write_src_names = ''
                write_src_ids = ''

                for index, source in enumerate(sources):
                    write_src_names += source.name + ('|' if index != len(sources)-1 else '')
                    write_src_ids += str(source.id_source) + ('|' if index != len(sources)-1 else '')

                writer.writerow({
                    'title': work.title,
                    'contributors': write_contributors,
                    'iswc': work.iswc,
                    'source': write_src_names,
                    'id': write_src_ids
                })
            return response
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
