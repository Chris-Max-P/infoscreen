import json
import requests
from datetime import datetime
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--station")

args = parser.parse_args()
station = args.station

# station = "Schneemannstraße" # "Mittersendling", "Höglwörther Straße", "Grünstraße", "Aidenbachstraße"

def station_url(station_name):
    return f"https://www.mvg.de/api/fahrinfo/location/queryWeb?q={station}"

def departure_url(station_id, footway=0):
    return f"https://www.mvg.de/api/fahrinfo/departure/{station_id}?footway={footway}"
    

current_station_data = requests.get(station_url(station))
current_station_data_json = current_station_data.text
id = json.loads(current_station_data.text)['locations'][0]['id']

current_departure_data = json.loads(requests.get(departure_url(id)).text)

deps = current_departure_data["departures"]
for dep in deps[:2]:
    delay_postfix = '0'
    if 'delay' in dep:
        delay_postfix = dep['delay']
    print(f"{dep['product']} {dep['label']} -> {dep['destination']}: {datetime.fromtimestamp(dep['departureTime']/1000.0).time()} + {delay_postfix}")
    