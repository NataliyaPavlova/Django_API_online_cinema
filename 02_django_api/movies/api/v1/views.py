from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, F
from django.http import JsonResponse
from django.views.generic.list import BaseListView

from movies.models import Filmwork, Person, Genre, PersonFilmwork, GenreFilmwork


class MoviesListApi(BaseListView):
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        queryset = Filmwork.objects.all().select_related('genre', 'person').values(
            'id',
            'title',
            'description',
            'creation_date',
            'rating',
            'type',
        ).annotate(
            genres=ArrayAgg(F('genre__name'), distinct=True),
            actors=ArrayAgg(F('person__full_name'), distinct=True, filter=Q(personfilmwork__role=PersonFilmwork.Role.ACTOR)),
            writers=ArrayAgg(F('person__full_name'), distinct=True, filter=Q(personfilmwork__role=PersonFilmwork.Role.WRITER)),
            directors=ArrayAgg(F('person__full_name'), distinct=True, filter=Q(personfilmwork__role=PersonFilmwork.Role.DIRECTOR)),
        )
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            'results': list(self.get_queryset()),
        }
        return context

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)
