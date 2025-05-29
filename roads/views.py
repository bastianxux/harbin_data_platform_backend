from .models import Way
from .models import RoadHourlyFlow, RoadDayFlow
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import BfmapWay, Highway
from shapely import wkb

@api_view(['GET'])
def list_all_bfmap_ways(request):
    all_ways = BfmapWay.objects.all()

    results = []
    for way in all_ways:
        coords = []
        if way.geom:
            shapely_geom = wkb.loads(bytes(way.geom.ewkb))  # 解析 LineString
            coords = [[pt[0], pt[1]] for pt in shapely_geom.coords]

        results.append({
            "gid": way.gid,
            "osm_id": way.osm_id,
            "class_id": way.class_id,
            "road_name": way.road_name,
            "coord_list": coords,
        })
    return Response(results)


@api_view(['GET'])
def filter_bfmap_ways(request):
    queryset = BfmapWay.objects.all()

    gid = request.GET.get('gid')
    osm_id = request.GET.get('osm_id')
    class_id = request.GET.get('class_id')
    road_name = request.GET.get('road_name')

    if gid:
        queryset = queryset.filter(gid=gid)
    if osm_id:
        queryset = queryset.filter(osm_id=osm_id)
    if class_id:
        queryset = queryset.filter(class_id=class_id)
    if road_name:
        queryset = queryset.filter(road_name__icontains=road_name)

    # 获取 class_id → highway name 映射
    class_ids = queryset.values_list('class_id', flat=True).distinct()
    highway_map = {
        h.id: h.name for h in Highway.objects.filter(id__in=class_ids)
    }

    results = []
    for way in queryset:
        coords = []
        if way.geom:
            try:
                shapely_geom = wkb.loads(bytes(way.geom.ewkb))
                coords = [[pt[0], pt[1]] for pt in shapely_geom.coords]
            except Exception as e:
                print(f"Error parsing geometry for gid {way.gid}: {e}")

        results.append({
            "gid": way.gid,
            "osm_id": way.osm_id,
            "class_id": way.class_id,
            "road_name": way.road_name,
            "highway_type": highway_map.get(way.class_id),
            "coord_list": coords
        })

    return Response(results)

@api_view(['GET'])
def list_ways(request):
    ways = Way.objects.all().values('id', 'tags', 'nodes')[:100]
    return Response(list(ways))
@api_view(['GET'])   
def road_flow(request):
    """
    /api/road-flow/?road_id=<ID>&date=<YYYY-MM-DD>
    返回: [{"hour":0,"traffic_cnt":12}, … ]
    """
    road_id = request.GET.get('road_id')
    day     = request.GET.get('date')           # yyyy-mm-dd

    if not (road_id and day):
        return Response({"detail": "road_id 和 date 都要传"}, status=400)

    qs = (RoadHourlyFlow.objects
            .filter(road_id=road_id, biz_date=day)
            .order_by('hour')
            .values('hour', 'traffic_cnt')[:24])   # 最多 24 行

    return Response(list(qs))

@api_view(['GET'])
def road_day_flow(request):
    """
    /api/road-day-flow/?road_ids=3,7,12&date=2015-01-03
    返回:
      [
        {"road_id":3,  "traffic_cnt":42},
        {"road_id":7,  "traffic_cnt": 0},
        {"road_id":12, "traffic_cnt":18}
      ]
    """
    road_ids_param = request.GET.get('road_ids')
    date_param     = request.GET.get('date')

    if not (road_ids_param and date_param):
        return Response(
            {"detail": "road_ids 和 date 都要传"},
            status=400
        )

    try:
        req_ids = [int(s) for s in road_ids_param.split(',') if s.strip()]
    except ValueError:
        return Response({"detail": "road_ids 必须是整数列表"}, status=400)

    # 查数据库
    qs = (RoadDayFlow.objects
            .filter(biz_date=date_param, road_id__in=req_ids)
            .values('road_id', 'traffic_cnt'))

    result_map = {rid: 0 for rid in req_ids}
    for row in qs:
        result_map[row['road_id']] = row['traffic_cnt']

    resp = [{'road_id': rid, 'traffic_cnt': result_map[rid]} for rid in req_ids]
    return Response(resp)