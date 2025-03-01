from django.urls import path
from search.views import SearchViewSet

urlpatterns = [
    path('', SearchViewSet.as_view({'get': 'search'}), name='search'),
]