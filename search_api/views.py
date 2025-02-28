from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework import status

from search_api.models import Actor, Film
from search_api.serializers import ActorSerializer, FilmSerializer


class SearchViewSet(ViewSet):
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get("q", "")

        if not query:
            return Response({"error": "Query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        actors = Actor.objects.filter(Q(first_name__icontains = query) | Q(last_name__icontains = query))
        actor_data = ActorSerializer(actors, many=True).data

        films = Film.objects.filter(Q(title__icontains = query))
        film_data = FilmSerializer(films, many=True).data
        
        return Response({
            "actors":actor_data,
            "films": film_data
        })