from rest_framework import serializers

from app.mutant.models import LogRequestStatistics, LogRequest
from library.genetics import AminoAcid


def amino_acid_validator(value):
    values = [x.name for x in AminoAcid]
    data_list = []

    if value:
        data_list = list(value)

    for v in data_list:
        if v not in values:
            raise serializers.ValidationError(
                f'You must provide correct amino'
                f' acid values with 6 digits:'
                f' {", ".join(values)}. Value sent: {value}.'
            )


class MutantSerializer(serializers.Serializer):
    dna = serializers.ListField(
        child=serializers.CharField(
            min_length=6,
            max_length=6,
            validators=[amino_acid_validator]
        ),
        allow_empty=False,
        allow_null=False,
    )


class LogRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogRequest
        fields = ('dna_sequence', 'mutant')


class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogRequestStatistics
        fields = (
            'count_human_dna',
            'count_mutant_dna',
            'ratio',
        )
