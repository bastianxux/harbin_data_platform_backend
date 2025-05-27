from .models import Way
from .models import RoadHourlyFlow
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import BfmapWay, Highway

@api_view(['GET'])
def list_all_bfmap_ways(request):
    ways = BfmapWay.objects.all().values(
        'gid', 'osm_id', 'class_id', 'road_name'
    )
    return Response(list(ways))


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

    ways = list(queryset.values('gid', 'osm_id', 'class_id', 'road_name'))

    # 加 highway 类型名（class_id 对应 highway.id）
    class_ids = set(w['class_id'] for w in ways if w['class_id'] is not None)
    highway_map = {
        h.id: h.name for h in Highway.objects.filter(id__in=class_ids)
    }

    for w in ways:
        w['highway_type'] = highway_map.get(w['class_id'], None)

    return Response(ways)

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