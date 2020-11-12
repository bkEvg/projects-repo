from rest_framework import serializers

from .models import Movie, Review, Rating, Actor

class MovieListSerializer(serializers.ModelSerializer):
    """Movie List Serializer"""
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'tagline', 'category', 'rating_user', 'middle_star')

class ReviewCreateSerializer(serializers.ModelSerializer):
    """Review Serializer"""
    class Meta:
        model = Review
        fields='__all__'


class FilterReviewSerializer(serializers.ListSerializer):
    """Filter of reviews only parents"""
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    """Review Serializer"""
    children = RecursiveSerializer(many=True)
    class Meta:
        list_serializer_class = FilterReviewSerializer
        model = Review
        fields = ('name', 'text', 'children')


class ActorListSerializer(serializers.ModelSerializer):
    """List of Actors and Directors serializer"""
    class Meta:
        model = Actor
        fields = ('id', 'name', 'image')


class ActorDetailSerializer(serializers.ModelSerializer):
    """Detail actor serializer"""

    class Meta:
        model = Actor
        fields = '__all__'


class MovieDetailSerializer(serializers.ModelSerializer):
    """ Movie Detail """
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = ActorListSerializer(read_only=True, many=True)
    actors = ActorListSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)


class CreateRatingSerializer(serializers.ModelSerializer):
    """Adding rating by user"""
    class Meta:
        model = Rating
        fields = ('star', 'movie')

    def create(self, validated_data):
        """Object goes in 'rating', True or False goes in '_' """
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get('star')}
        )
        return rating
