from typing import Dict, Any

import openmeteo_requests
import requests
import json
import requests_cache
import pandas as pd
from retry_requests import retry


def list_city():
    "list CapitalCity"
    with open('city.txt', 'r') as f:
        data = dict(json.load(f))
    return list(map(lambda x: x.split(' (')[0], [data[x] for x in data]))


def lat_long(city):
    " Координаты по городу"
    lat = []
    long = []
    new_city = []
    for x in city:
        url_city = f"https://geocoding-api.open-meteo.com/v1/search?name={x}&count=1&language=en&format=json"
        city_coord = requests.get(url_city)
        data = json.loads(city_coord.text)
        if data.get("results") is not None:
            lat.append(data["results"][0].get("latitude"))
            long.append(data["results"][0].get("longitude"))
            new_city.append(x)

    return lat, long, new_city


def temp_data(lat, long, city):
    """

    :param *lat:
    :param *long:
    :type city: object
    """
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://archive-api.open-meteo.com/v1/archive"
    # https://archive-api.open-meteo.com/v1/archive?latitude=58.0105,55.7522,51.5085&longitude=56.2502,37.6156,-0.1257&start_date=2024-03-11&end_date=2024-04-11&daily=temperature_2m_mean

    params: dict[str, str | Any] = {
            "latitude": lat,
            "longitude": long,
            "start_date": "2024-03-11",
            "end_date": "2024-04-11",
            "daily": "temperature_2m_mean"
        }

    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    data = {}
    for i in range(len(city)):
        print(f'{i}, осталось {len(city)}')
        response = responses[i]
        # print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
        # print(f"Elevation {response.Elevation()} m asl")
        # print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
        # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process daily data. The order of variables needs to be the same as requested.
        daily = response.Daily()
        daily_temperature_2m_mean = daily.Variables(0).ValuesAsNumpy()

        daily_data = {"date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        ), city[i]: daily_temperature_2m_mean}
        data.update(daily_data)

    daily_dataframe = pd.DataFrame(data=data)
    daily_dataframe.to_csv('daily_data.csv')






city = list_city()
lat, long, city = lat_long(city)
temp_data(lat, long, city)
