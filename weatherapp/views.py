from django.shortcuts import render
import requests
from .forms import FeedbackForm
from django.http import HttpResponseRedirect
from django.views import View
# Create your views here.
class FeedbackView(View):

    def get(self, request):
        form = FeedbackForm()
        return render(request, 'weatherapp/feedback.html', context={'form': form})

    def post(self, request):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('home')
        return render(request, 'weatherapp/feedback.html', context={'form': form})

def index(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'Москва'



    appid = 'af36c188eb414fbdb56101114232303 '
    lnk = f'http://api.weatherapi.com/v1/current.json?key={appid}&q={city}&aqi=yes&lang=ru'
    lnk2 = f'http://api.weatherapi.com/v1/astronomy.json?key={appid}&q={city}&dt='
    r = requests.get(url=lnk)
    r1 = requests.get(url=lnk2)
    res = r.json()
    res1 = r1.json()
    try:
        data = {
            'city': city,
            'day': res['location']['localtime'],
            'description': res['current']['condition']['text'],
            'icon': res['current']['condition']['icon'],
            'temp': res['current']['temp_c'],
            'humidity': res['current']['humidity'],
            'pressure': res['current']['pressure_mb'] * 0.75,
            'wind': f"{res['current']['wind_kph'] * 0.27:.2f}",
            'gust': f"{res['current']['gust_kph'] * 0.27:.2f}",
            'sunrise': res1['astronomy']['astro']['sunrise'],
            'sunset': res1['astronomy']['astro']['sunset'],
        }
        return render(request, 'weatherapp/index.html', context=data)
    except KeyError:
        return HttpResponseRedirect('home')


def get_forecast(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'Москва'
    appid = 'af36c188eb414fbdb56101114232303 '
    lnk = f'http://api.weatherapi.com/v1/forecast.json?key={appid}&q={city}&days=10&aqi=no&alerts=no&lang=ru'
    r = requests.get(url=lnk)
    res = r.json()
    try:
        forecast = res['forecast']['forecastday']
        for i in range(10):
            forecast[i]['num'] = i
        data = {
            'city': city,
            'days': forecast,
        }
        return render(request, 'weatherapp/get_forecast.html', context=data)
    except KeyError:
        return HttpResponseRedirect('forecast')

def get_hour_forecast(request, num_day: int):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'Москва'
    appid = 'af36c188eb414fbdb56101114232303 '
    lnk = f'http://api.weatherapi.com/v1/forecast.json?key={appid}&q={city}&days=10&aqi=no&alerts=no&lang=ru'
    r = requests.get(url=lnk)
    res = r.json()

    data = {
        'city': city,
        'day': res['forecast']['forecastday'][num_day]['hour']
    }
    return render(request, 'weatherapp/hour_forecast.html', context=data)


def get_info_of_airquality(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'Москва'
    appid = 'af36c188eb414fbdb56101114232303 '
    lnk = f'http://api.weatherapi.com/v1/current.json?key={appid}&q={city}&aqi=yes'
    r = requests.get(url=lnk)
    res = r.json()
    try:
        data = {
            'city': city,
            'day': res['location']['localtime'],
            'pm25': round(res['current']['air_quality']['pm2_5'], 2),
            'no2': round(res['current']['air_quality']['no2'], 2),
            'o3': round(res['current']['air_quality']['o3'], 2),
            'so2': round(res['current']['air_quality']['so2']),
            'co': round(res['current']['air_quality']['co'], 2)


        }
        return render(request, 'weatherapp/airquality.html', context=data)
    except KeyError:
        return HttpResponseRedirect('airquality')

# def flying_conditions(request):
#
#     if 'city' in request.POST:
#         city = request.POST['city']
#     else:
#         city = 'Москва'
#
#
#
#     appid = 'af36c188eb414fbdb56101114232303 '
#     lnk = f'http://api.weatherapi.com/v1/current.json?key={appid}&q={city}&aqi=no'
#
#     r = requests.get(url=lnk)
#     res = r.json()
#     description = res['current']['condition']['text']
#     wind = f"{res['current']['wind_kph'] * 0.27:.2f}",
#     gust = f"{res['current']['gust_kph'] * 0.27:.2f}",
#     humidity = res['current']['humidity']
#     temp = res['current']['temp_c']
#     data = {
#         'city': city,
#         'day': res['location']['localtime'],
#         'icon': res['current']['condition']['icon'],
#         'description': description,
#         'humidity': humidity,
#         'temp': temp,
#         'wind': wind,
#         'gust': gust,
#     }
#     return render(request, 'weatherapp/flycond.html', context=data)










