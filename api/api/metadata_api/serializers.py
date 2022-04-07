from rest_framework import serializers

from api.metadata_api.models import Dataset, Table, Column


class DatasetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dataset
        fields = ["url", "name", "description"]


class TableSerializer(serializers.HyperlinkedModelSerializer):
    dataset = DatasetSerializer()

    class Meta:
        model = Table
        fields = ["url", "name", "description", "dataset"]


class ColumnSerializer(serializers.HyperlinkedModelSerializer):
    table = TableSerializer()

    class Meta:
        model = Column
        fields = ["url", "name", "description", "table"]
