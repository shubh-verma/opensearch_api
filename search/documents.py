from django_opensearch_dsl import Document
from django_opensearch_dsl.registries import registry
from search.models import Actor, Film

# Define the Actor index
@registry.register_document
class ActorDocument(Document):
    class Index:
        name = 'actors'  # Name of the OpenSearch index

    class Django:
        model = Actor
        fields = ['first_name', 'last_name']  # Fields to index

# Define the Film index
@registry.register_document
class FilmDocument(Document):
    class Index:
        name = 'films'  # Name of the OpenSearch index

    class Django:
        model = Film
        fields = ['title']  # Fields to index
