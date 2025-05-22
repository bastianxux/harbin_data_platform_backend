from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Way

@api_view(['GET'])
def list_ways(request):
    ways = Way.objects.all().values('id', 'tags', 'nodes')[:100]
    return Response(list(ways))