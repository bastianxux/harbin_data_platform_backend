from .models import Way
from .models import RoadHourlyFlow
from .models import RoadDailyCount
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import BfmapWay, Highway
from shapely import wkb


@api_view(["GET"])
def list_all_bfmap_ways(request):
    all_ways = BfmapWay.objects.all()

    results = []
    for way in all_ways:
        coords = []
        if way.geom:
            shapely_geom = wkb.loads(bytes(way.geom.ewkb))  # 解析 LineString
            coords = [[pt[0], pt[1]] for pt in shapely_geom.coords]

        results.append(
            {
                "gid": way.gid,
                "osm_id": way.osm_id,
                "class_id": way.class_id,
                "road_name": way.road_name,
                "coord_list": coords,
            }
        )
    return Response(results)


@api_view(["GET"])
def filter_bfmap_ways(request):
    queryset = BfmapWay.objects.all()

    gid = request.GET.get("gid")
    osm_id = request.GET.get("osm_id")
    class_id = request.GET.get("class_id")
    road_name = request.GET.get("road_name")

    if gid:
        queryset = queryset.filter(gid=gid)
    if osm_id:
        queryset = queryset.filter(osm_id=osm_id)
    if class_id:
        queryset = queryset.filter(class_id=class_id)
    if road_name:
        queryset = queryset.filter(road_name__icontains=road_name)

    # 获取 class_id → highway name 映射
    class_ids = queryset.values_list("class_id", flat=True).distinct()
    highway_map = {h.id: h.name for h in Highway.objects.filter(id__in=class_ids)}

    results = []
    for way in queryset:
        coords = []
        if way.geom:
            try:
                shapely_geom = wkb.loads(bytes(way.geom.ewkb))
                coords = [[pt[0], pt[1]] for pt in shapely_geom.coords]
            except Exception as e:
                print(f"Error parsing geometry for gid {way.gid}: {e}")

        results.append(
            {
                "gid": way.gid,
                "osm_id": way.osm_id,
                "class_id": way.class_id,
                "road_name": way.road_name,
                "highway_type": highway_map.get(way.class_id),
                "coord_list": coords,
            }
        )

    return Response(results)


@api_view(["GET"])
def list_ways(request):
    ways = Way.objects.all().values("id", "tags", "nodes")[:100]
    return Response(list(ways))


@api_view(["GET"])
def road_flow(request):
    """
    /api/road-flow/?road_id=<ID>&date=<YYYY-MM-DD>
    返回: [{"hour":0,"traffic_cnt":12}, … ]
    """
    road_id = request.GET.get("road_id")
    day = request.GET.get("date")  # yyyy-mm-dd

    if not (road_id and day):
        return Response({"detail": "road_id 和 date 都要传"}, status=400)

    qs = (
        RoadHourlyFlow.objects.filter(road_id=road_id, biz_date=day)
        .order_by("hour")
        .values("hour", "traffic_cnt")[:24]
    )  # 最多 24 行

    return Response(list(qs))


@api_view(["GET"])
def top_n_roads_by_day(request):
    """
    /api/top-roads/?date=<YYYY-MM-DD>&n=<count>
    返回: [{"road_id": "xyz", "trip_count": 100}, ... ]
    """
    target_date = request.GET.get("date")  # yyyy-mm-dd
    top_n_str = request.GET.get("n")

    if not (target_date and top_n_str):
        return Response({"detail": "date 和 n 都是必须的参数"}, status=400)

    try:
        top_n = int(top_n_str)
        if top_n <= 0:
            raise ValueError("n 必须是正整数")
    except ValueError as e:
        return Response({"detail": f"无效的n参数: {e}"}, status=400)

    # 假设模型名为 RoadDailyCount，并且它有一个 date 字段和一个 trip_count 字段
    # 以及一个 road_id 字段 (通常是 CharField 或 ForeignKey)
    qs = (
        RoadDailyCount.objects.filter(date=target_date)
        .order_by("-trip_count")
        .values("road_id", "trip_count")[:top_n]
    )

    return Response(list(qs))
