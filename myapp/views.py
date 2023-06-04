from django.shortcuts import render
import requests
import datetime
import logging
logger = logging.getLogger(__name__)

def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    current_response = requests.get(current_weather_url.format(city, api_key)).json()
    logger.debug('API current_response: %s', current_response) 
    lat, lon = current_response['coord']['lat'], current_response['coord']['lon']
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()
    logger.debug("API response :%s", forecast_response)

    weather_data = {
        'city': city,
        'temperature': round(current_response['main']['temp'] - 273.15, 2),
        'description': current_response['weather'][0]['description'],
        'icon': current_response['weather'][0]['icon'],
    }

    daily_forecasts = []
    daily_data = forecast_response.get('daily', [])
    for daily_data in daily_data:
        daily_forecasts.append({
            'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
            'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
            'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
            'description': daily_data['weather'][0]['description'],
            'icon': daily_data['weather'][0]['icon'],
        })

    return weather_data, daily_forecasts




def index(request):
    api_key = '1754d5cc1580e244fab3fc30f7a5824e'
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'


    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, api_key, current_weather_url, forecast_url)

        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, api_key, current_weather_url, forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None

        context = {
            'weather_data1': weather_data1,
            'daily_forecasts1': daily_forecasts1,
            'weather_data2': weather_data2,
            'daily_forecasts2': daily_forecasts2,
        }

        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')


