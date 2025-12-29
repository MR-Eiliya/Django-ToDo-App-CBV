from django.views import View
from django.http import JsonResponse
from django.core.cache import cache
import requests

class WeatherAPIView(View):
    API_KEY = "678bea87d22e54963d6fced6a8039821"
    CITY = "Paris"
    CACHE_TIMEOUT = 20 * 60 

    def get(self, request, *args, **kwargs):
        cache_key = f"weather_{self.CITY.lower()}"
        data = cache.get(cache_key)
        if data:
            return JsonResponse(data)

        url = f"http://api.openweathermap.org/data/2.5/weather?q={self.CITY}&appid={self.API_KEY}&units=metric"
        
        try:
            response = requests.get(url, timeout=5)  #
            response.raise_for_status()  
            data = response.json()
            cache.set(cache_key, data, self.CACHE_TIMEOUT)
            return JsonResponse(data)
        except requests.RequestException as e:
            print(f"Weather API error: {e}")
            return JsonResponse({'error':'cannot fetch weather data'}, status=500)
