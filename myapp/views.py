from django.shortcuts import render
import requests

def fetch_weather_and_forecast(city, api_key, current_weather_url):
    current_response = requests.get(current_weather_url.format(city, api_key)).json()
    # logger.debug('API current_response: %s', current_response) 

    weather_data = {
        'city': city,
        'temperature': round(current_response['main']['temp'] - 273.15, 2),
        'description': current_response['weather'][0]['description'],
        'icon': current_response['weather'][0]['icon'],
    }


    return weather_data




def index(request):
    api_key = '<API KEY>'
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'


    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        weather_data1= fetch_weather_and_forecast(city1, api_key, current_weather_url)

        if city2:
            weather_data2 = fetch_weather_and_forecast(city2, api_key, current_weather_url)
        else:
            weather_data2 = None

        context = {
            'weather_data1': weather_data1,
            'weather_data2': weather_data2,
        }

        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')


