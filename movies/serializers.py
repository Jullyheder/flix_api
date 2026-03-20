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


class MovieSerializer(ModelSerializer):
    rate = SerializerMethodField(read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'

    def get_rate(self, obj):
        rate = obj.reviews.aggregate(Avg('stars'))['stars__avg']

        if not rate:
            return None

        return round(rate, 1)

    def validate_release_date(self, value):
        if value.year < 1990:
            raise ValidationError('A data de lançamento deve ser maior que 1990.')
        return value

    def validate_resume(self, value):
        if len(value) > 200:
            raise ValidationError('O resumo deve ter no máximo 200 caracteres.')
        return value


class MovieStatsSerializer(Serializer):
    total_movies = IntegerField()
    movies_by_genre = ListField()
    total_reviews = IntegerField()
    average_rating = FloatField()
