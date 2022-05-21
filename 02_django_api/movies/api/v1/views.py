from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, F
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from django.core.paginator import Paginator

from movies.models import Filmwork, Person, Genre, PersonFilmwork, GenreFilmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']
    paginate_by = 50

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
            actors=ArrayAgg(F('person__full_name'), distinct=True,
                            filter=Q(personfilmwork__role=PersonFilmwork.Role.ACTOR)),
            writers=ArrayAgg(F('person__full_name'), distinct=True,
                             filter=Q(personfilmwork__role=PersonFilmwork.Role.WRITER)),
            directors=ArrayAgg(F('person__full_name'), distinct=True,
                               filter=Q(personfilmwork__role=PersonFilmwork.Role.DIRECTOR)),
        )
        return queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset)
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def context_data(self, queryset, pk):
        return queryset.get(id=pk)

    def get(self, request, pk):
        return self.render_to_response(self.context_data(self.get_queryset(), pk=pk))
    