import random
import time
import requests

be_url = "http://localhost:8080"
be_rooms_url = f"{be_url}/rooms"
influx_url = 'http://localhost:8086'
influx_username = 'admin'
influx_password = 'password'


def get_rooms_from_be(url_endpoint_rooms):
    response = requests.get(url_endpoint_rooms)
    data = response.json()
    return data


def process_data_be():
    rooms_data = get_rooms_from_be(be_rooms_url)
    for room in rooms_data:
        current_time = int(round(time.time() * 1000000000))
        room_split = room["id"].split(":")
        retention = room_split[1]  # nome Home
        measurement = room_split[2]
        humidity = random.randint(0, 100)
        temperature = random.randint(-10, 40)
        influx_point = build_influx_point(measurement, temperature, humidity, current_time)
        write_data(room["usernameID"], retention, influx_point)


def write_data(database, retention, influx_point):
    influx_write_url = f"{influx_url}/write?db={database}&rp={retention}"

    response = requests.post(influx_write_url, data=influx_point)
    if response.status_code != 204:
        print(f"Failed to write data to InfluxDB: {response.content}")


def build_influx_point(measurement, temperature, humidity, current_time):
    return f"{measurement} temperature={temperature},humidity={humidity} {current_time}"


process_data_be()
