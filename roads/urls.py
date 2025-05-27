from django.urls import path
from . import views

urlpatterns = [
    path('ways/', views.list_ways),
    path('road-flow/',  views.road_flow),
    path('bfmap_ways/', views.list_all_bfmap_ways),
    path('bfmap_ways/filter/', views.filter_bfmap_ways),
    # 新增：按天取路段 24h 流量
]