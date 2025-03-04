from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from opensearchpy.helpers.response import Response as RR
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework import status

# from search.models import Actor, Film
from search.serializers import ActorSerializer, FilmSerializer
from search.documents import ActorDocument, FilmDocument


class ActorSearchViewSet(ViewSet):
    @action(detail=False, methods=['get'])
    def search(self, request):
        actor_search = request.query_params.get("q", "")

        if not actor_search:
            return Response({"error": "Query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
        actors = ActorDocument.search().query(
            "multi_match",
            query=actor_search,
            fields=["first_name", "last_name"],
            fuzziness="AUTO",
        )

        try:
            response: RR = actors.execute()
            serialized_response = ActorSerializer(response, many=True)
            return Response(serialized_response.data, status=status.HTTP_200_OK)

        except Exception:
            return Response({"error": "Failed to retrieve actor data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class FilmsSearchViewSet(ViewSet):
    @action(detail=False, methods=['get'])
    def search(self, request):
        film_search = request.query_params.get("q", "")

        if not film_search:
            return Response({"error": "Query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        films = FilmDocument.search().query(
            "multi_match",
            query=film_search,
            fields=["title"],
            fuzziness="AUTO",
        )

        # film_data = films.filter(Q(title__icontains = film_search))

        try:
            response: RR = films.execute()
            serialized_response = FilmSerializer(response, many=True)
            print(response)
            return Response(serialized_response.data, status=status.HTTP_200_OK)

        except:
            return Response({"error": "Failed to retrieve film data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
    # @action(detail=False, methods=['get'])
    # def search(self, request):
    #     actor_search = request.query_params.get("q", "")

    #     if not actor_search:
    #         return Response({"error": "Query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    #     actors = Actor.objects.filter(Q(first_name__icontains = actor_search) | Q(last_name__icontains = actor_search))
    #     actor_data = ActorSerializer(actors, many=True).data

    #     return Response({
    #         "actors":actor_data,
    #     })
    
    
    # @action(detail=False, methods=['get'])
    # def search(self, request):
    #     film_search = request.query_params.get("q", "")

    #     if not film_search:
    #         return Response({"error": "Query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    #     films = Film.objects.filter(Q(title__icontains = film_search))
    #     film_data = FilmSerializer(films, many=True).data
        
    #     return Response({
    #         "films": film_data
    #     })