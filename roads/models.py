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

class RoadHourlyFlow(models.Model):
    biz_date     = models.DateField()
    road_id      = models.BigIntegerField()
    hour         = models.PositiveSmallIntegerField()   # 0-23
    traffic_cnt  = models.IntegerField()

    class Meta:
        db_table = 'road_hourly_flow'   # 就是那个物化视图
        managed  = False                # 告诉 Django：不用它来建表
        unique_together = (('biz_date', 'road_id', 'hour'),)