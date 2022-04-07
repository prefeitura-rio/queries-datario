from django.db.models import CharField, TextField
from django.db.models import Q
from rest_framework import viewsets
from rest_framework import permissions

from api.metadata_api.models import Dataset, Table, Column
from api.metadata_api.serializers import (
    DatasetSerializer,
    TableSerializer,
    ColumnSerializer,
)


class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all().order_by("name")
    serializer_class = DatasetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all().order_by("name")
    serializer_class = TableSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ColumnViewSet(viewsets.ModelViewSet):
    queryset = Column.objects.all().order_by("name")
    serializer_class = ColumnSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SearchViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TableSerializer

    def get_queryset(self):
        query_text = self.request.query_params.get("q", "")

        # First we query for columns that match the query text
        fields = [
            f
            for f in Column._meta.fields
            if (isinstance(f, CharField) or isinstance(f, TextField))
        ]
        queries = [Q(**{f"{f.name}__icontains": query_text}) for f in fields]
        qs = Q()
        for query in queries:
            qs = qs | query
        tables_from_columns = set([c.table for c in Column.objects.filter(qs)])

        # Then we query for tables that match the query text
        fields = [
            f
            for f in Table._meta.fields
            if (isinstance(f, CharField) or isinstance(f, TextField))
        ]
        queries = [Q(**{f"{f.name}__icontains": query_text}) for f in fields]
        qs = Q()
        for query in queries:
            qs = qs | query
        tables_from_tables = set([t for t in Table.objects.filter(qs)])

        # And finally we query for datasets that match the query text
        fields = [
            f
            for f in Dataset._meta.fields
            if (isinstance(f, CharField) or isinstance(f, TextField))
        ]
        queries = [Q(**{f"{f.name}__icontains": query_text}) for f in fields]
        qs = Q()
        for query in queries:
            qs = qs | query
        datasets = Dataset.objects.filter(qs)
        # Get all tables from these datasets
        tables_from_datasets = set([t for d in datasets for t in d.tables.all()])

        # Finally, we merge the sets of tables from columns, tables and datasets
        tables = tables_from_columns | tables_from_tables | tables_from_datasets

        return list(tables)
