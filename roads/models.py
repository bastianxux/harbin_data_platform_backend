from django.db import models
from django.contrib.postgres.fields import HStoreField
from django.contrib.postgres.fields import ArrayField
from django.contrib.gis.db import models as gis_models

class BfmapWay(models.Model):
    gid = models.BigAutoField(primary_key=True)
    osm_id = models.BigIntegerField(null=True)
    class_id = models.IntegerField(null=True)
    source = models.BigIntegerField(null=True)
    target = models.BigIntegerField(null=True)
    length = models.FloatField(null=True)
    reverse = models.FloatField(null=True)
    maxspeed_forward = models.IntegerField(null=True)
    maxspeed_backward = models.IntegerField(null=True)
    priority = models.FloatField(null=True)
    geom = gis_models.LineStringField(srid=4326, null=True)
    road_name = models.TextField(null=True)

    class Meta:
        db_table = 'bfmap_ways'
        managed = False

class Highway(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    priority = models.FloatField(null=True)
    maxspeed = models.IntegerField(null=True)

    class Meta:
        db_table = 'highway'
        managed = False


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

class RoadDayFlow(models.Model):
    biz_date    = models.DateField()
    road_id     = models.BigIntegerField()
    traffic_cnt = models.IntegerField()

    class Meta:
        db_table  = 'road_day_flow'   # 你的物化视图名称
        managed   = False             # 别让 migrate 去动它
        unique_together = (('biz_date', 'road_id'),)


class RoadDailyCount(models.Model):
    road_id = models.TextField()
    date = models.DateField()
    trip_count = models.BigIntegerField()

    class Meta:
        db_table = "road_daily_count"
        managed = False


class RoadHourlyCount(models.Model):
    road_id = models.TextField()
    hour_of_day = models.IntegerField()  # 0-23
    trip_count = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = "road_hourly_count"
        unique_together = (("road_id", "hour_of_day"),)

class RoadPeakPeriodCount(models.Model):
    road_id = models.TextField()
    peak_period = models.TextField()  # 取值为 Morning Peak, Normal, Evening Peak
    trip_count = models.BigIntegerField()

    class Meta:
        db_table = 'road_peak_period_count'
        managed = False

class RoadHighwayMapping(models.Model):
    road_id = models.BigIntegerField()
    highway_name = models.TextField()
    highway_id = models.IntegerField()

    class Meta:
        db_table = 'road_highway_mapping'
        managed = False
