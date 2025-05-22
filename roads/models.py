from django.db import models
from django.contrib.postgres.fields import HStoreField
from django.contrib.postgres.fields import ArrayField


class Way(models.Model):
    id = models.BigIntegerField(primary_key=True)
    tags = HStoreField()
    nodes = ArrayField(models.BigIntegerField())

    class Meta:
        db_table = 'ways'
        managed = False