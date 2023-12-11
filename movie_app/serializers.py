from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

        def get_category(self, movie):
            try:
                return movie.category.name
            except:
                return 'no category'

        def get_reviews(self, movie):
            serializer = ReviewSerializer(Review.objects.filter(author_isnull=False, movie=movie), many=True),
            return serializer.data
