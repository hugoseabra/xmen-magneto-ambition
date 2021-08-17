import json

from django.forms.models import model_to_dict
from django.conf import settings
from cacheops import file_cache, CacheMiss
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from library.genetics import Analyser, DNA, CodonPair, AminoAcid
from .serializers import (
    StatisticsSerializer,
    LogRequestSerializer,
    MutantSerializer,
)


class MutantViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = MutantSerializer
    queryset = LogRequestSerializer.Meta.model.objects.get_queryset()

    def create(self, request, *args, **kwargs):
        mutant_serializer = MutantSerializer(data=request.data)
        mutant_serializer.is_valid(raise_exception=True)

        dna = DNA()

        for seq in mutant_serializer.validated_data['dna']:
            dna.append(CodonPair(
                (AminoAcid[seq[0]], AminoAcid[seq[1]], AminoAcid[seq[2]]),
                (AminoAcid[seq[3]], AminoAcid[seq[4]], AminoAcid[seq[5]]),
            ))

        if dna.is_valid() is False:
            return Response(
                {'message': 'DNA is not valid.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        analyser = Analyser()
        is_mutant = analyser.is_mutant(dna)

        log = LogRequestSerializer(data={
            'mutant': is_mutant,
            'dna_sequence': json.dumps(mutant_serializer.validated_data['dna'])
        })
        log.is_valid(raise_exception=True)
        self.perform_create(log)

        if is_mutant is False:
            return Response(
                {'message': 'DNA is not mutant.'},
                status=status.HTTP_403_FORBIDDEN
            )

        return Response(
            {
                'message': 'DNA is mutant',
                'content': mutant_serializer.validated_data
            },
            status=status.HTTP_200_OK,
            headers=self.get_success_headers(mutant_serializer.validated_data)
        )


class StatisticsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = StatisticsSerializer
    queryset = StatisticsSerializer.Meta.model.objects.get_queryset()
    http_method_names = ['get']

    def get_object(self):
        queryset = self.get_queryset()
        model_class = StatisticsSerializer.Meta.model

        instance = None

        try:
            data = file_cache.get(settings.STATS_CACHE_KEY)
            instance = model_class(**data)
        except CacheMiss:
            pass

        if instance is None:
            try:
                instance = queryset.get(pk=1)
            except model_class.DoesNotExist:
                instance = model_class(
                    count_human_dna=0,
                    count_mutant_dna=0,
                    ratio=0.0,
                )

            data = {
                'count_human_dna': instance.count_human_dna,
                'count_mutant_dna': instance.count_mutant_dna,
                'ratio': instance.ratio
            }
            file_cache.set(settings.STATS_CACHE_KEY, data, timeout=60 * 60)

        return instance

    def list(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
