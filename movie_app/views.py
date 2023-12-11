from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie_app.serializers import *
from .models import *
from rest_framework import status


@api_view(['GET'])
def director_list_view(request):
    directors = Director.objects.all()
    data = []
    for director in directors:
        director_data = DirectorSerializer(director).data
        director_data['movies_count'] = Movie.objects.filter(director=director).count()
        data.append(director_data)
    return Response(data)


@api_view(['GET'])
def director_detail_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': "Режиссер не найден"})
    data = DirectorSerializer(director).data
    return Response(data=data)


@api_view(['GET'])
def movie_list_view(request):
    movies = Movie.objects.all()
    data = MovieSerializer(movies, many=True).data
    return Response(data)


@api_view(['GET'])
def movie_detail_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': "Фильм не найден"})
    data = MovieSerializer(movie).data
    return Response(data=data)


@api_view(['GET'])
def review_list_view(request):
    movies = Movie.objects.all()
    data = []
    for movie in movies:
        movie_data = MovieSerializer(movie).data
        movie_data['reviews'] = ReviewSerializer(movie.reviews, many=True).data
        data.append(movie_data)

    # Calculate average rating
    all_reviews = Review.objects.all()
    total_stars = sum([int(review.stars) for review in all_reviews])
    average_rating = total_stars / all_reviews.count() if all_reviews.count() > 0 else 0

    return Response({'movies': data, 'average_rating': average_rating})


@api_view(['GET'])
def review_detail_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': "Отзыв не найден"})
    data = ReviewSerializer(review).data
    return Response(data=data)
