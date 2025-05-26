from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Way
from .models import RoadHourlyFlow
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