from django.db.models import Avg
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    SerializerMethodField,
    Serializer,
    IntegerField,
    ListField,
    FloatField
)
from movies.models import Movie
from actors.serializers import ActorSerializer
from genres.serializers import GenreSerializer


class MovieSerializer(ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'

    def validate_release_date(self, value):
        if value.year < 1970:
            raise ValidationError('A data de lançamento deve ser maior que 1990.')
        return value

    def validate_resume(self, value):
        if len(value) > 500:
            raise ValidationError('O resumo deve ter no máximo 200 caracteres.')
        return value


class MovieListDetailSerializer(ModelSerializer):
    actors = ActorSerializer(many=True)
    genre = GenreSerializer()
    rate = SerializerMethodField(read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'genre',
            'actors',
            'release_date',
            'rate',
            'resume'
        ]

    def get_rate(self, obj):
        rate = obj.reviews.aggregate(Avg('stars'))['stars__avg']

        if not rate:
            return None

        return round(rate, 1)


class MovieStatsSerializer(Serializer):
    total_movies = IntegerField()
    movies_by_genre = ListField()
    total_reviews = IntegerField()
    average_rating = FloatField()
