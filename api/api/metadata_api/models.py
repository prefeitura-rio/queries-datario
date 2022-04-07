from django.db import models


class Dataset(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"Dataset {self.name}"

    def __repr__(self) -> str:
        return self.__str__()


class Table(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    dataset = models.ForeignKey(
        Dataset, on_delete=models.CASCADE, related_name="tables"
    )

    def __str__(self) -> str:
        return f"Table {self.dataset.name}.{self.name}"

    def __repr__(self) -> str:
        return self.__str__()


class Column(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="columns")

    def __str__(self) -> str:
        return f"Column {self.table.dataset.name}{self.table.name}.{self.name}"

    def __repr__(self) -> str:
        return self.__str__()
