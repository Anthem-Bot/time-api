import requests
import json
from flask import Flask, request
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

geolocator = Nominatim(
    user_agent="Anthem Time-API https://github.com/Anthem-Bot/time-api")
app = Flask(__name__)
config = open('config.json')


@app.route('/')
def main():
    location = request.args.get('location')
    if location is None:
        return {"msg": "Please specify a location"}

    result = getLocation(location)
    time = getTime(result)
    return {
        "abbreviation": time['abbreviation'],
        "time": time['datetime'],
        "unixtime": time['unixtime'],
        "timezone": time['timezone'],
        "dst": {
            "observes_dst": time['dst'],
            "dst_from": time['dst_from'],
            "dst_until": time['dst_until'],
            "dst_offset": time['dst_offset']
        },
        "utc": {
            "time": time['utc_datetime'],
            "offset": time['utc_offset']
        }
    }


app.run('0.0.0.0', json.load(config)['port'])


def getLocation(location):
    cords = geolocator.geocode(location)

    obj = TimezoneFinder()
    result = obj.timezone_at(lng=cords.longitude, lat=cords.latitude)

    return result


def getTime(timezone):
    res = requests.get(f"http://worldtimeapi.org/api/timezone/{timezone}")
    data = res.text

    return json.loads(data)
