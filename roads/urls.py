from django.urls import path
from .views import list_ways

urlpatterns = [
    path('ways/', list_ways),
]