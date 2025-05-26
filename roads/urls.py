from django.urls import path
from .views import list_ways, road_flow

urlpatterns = [
    path('ways/', list_ways),
    path('road-flow/',  road_flow),       # 新增：按天取路段 24h 流量
]