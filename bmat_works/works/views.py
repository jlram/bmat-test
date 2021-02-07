import csv
import io

from django.db.models import Q
from django.shortcuts import get_object_or_404

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
        """Retrieves Work by ISWC instead of ID"""
        work = get_object_or_404(self.queryset, iswc=pk)
        serializer = WorkSerializer(work)
        return Response(serializer.data)


    def update(self, request, *args, **kwargs):
        """Updates Work by ISWC instead of ID"""
        instance = self.queryset.get(iswc=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Destroys Work by ISWC instead of ID"""
        work = get_object_or_404(self.queryset, iswc=pk)
        work.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ContributorViewSet(viewsets.ModelViewSet):
    """Work CRUD"""
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

    def update(self, request, *args, **kwargs):
        """Partial update for Contributor"""
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class SourceViewSet(viewsets.ModelViewSet):
    """Work CRUD"""
    queryset = Source.objects.all()
    serializer_class = SourceSerializer

    def update(self, request, *args, **kwargs):
        """Partial update for Source"""
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ImportCSVViewSet(viewsets.ViewSet):
    """
        :param `file`: .csv file
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
                            # Best way to compare Querysets
                            if set(work.contributors.all()) == set(Contributor.objects.filter(filter)):
                                add_relations(work, None, (no_iswc_work[3], no_iswc_work[4]))

            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No file attached'}, status=status.HTTP_406_NOT_ACCEPTABLE)
