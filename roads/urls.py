from django.urls import path
from . import views

urlpatterns = [
    path('ways/', views.list_ways),
    path('road-flow/',  views.road_flow),
    path('road-day-flow/', views.road_day_flow),
    path('bfmap_ways/', views.list_all_bfmap_ways),
    path('bfmap_ways/filter/', views.filter_bfmap_ways),
    path('top-roads/', views.top_n_roads_by_day),
    path('top-roads-by-hour/', views.top_n_roads_by_hour),
    path('top-roads-by-peak/', views.top_n_roads_by_peak_period),
    path('roads-by-highway-type/', views.roads_by_highway_type),
    path('top-roads-by-duration/', views.top_n_roads_by_duration_category),
    # 新增：按天取路段 24h 流量
]