from django.urls import path
from search_api.views import SearchViewSet

urlpatterns = [
    path('', SearchViewSet.as_view({'get': 'search'}), name='search'),
]