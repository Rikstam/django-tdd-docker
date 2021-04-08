from django.urls import path
from rest_framework import routers

from .views import MovieViewSet

router = routers.DefaultRouter()
router.register(r'api/movies', MovieViewSet, basename='movie')

urlpatterns = router.urls

"""urlpatterns = [
    path("api/movies/", MovieList.as_view()),
    path("api/movies/<int:pk>/", MovieDetail.as_view()),
]"""
