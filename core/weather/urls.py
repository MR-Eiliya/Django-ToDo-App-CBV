from django.urls import path
from .views import WeatherAPIView

urlpatterns = [
    path("api/", WeatherAPIView.as_view(), name="weather-api"),
] 