import random
import time
import requests
import argparse


def get_rooms_from_be(url_endpoint_rooms):
    response = requests.get(url_endpoint_rooms + "/rooms")
    data = response.json()
    return data


def process_data_be(be_rooms_url, influx_url):
    rooms_data = get_rooms_from_be(be_rooms_url)
    for room in rooms_data:
        current_time = int(round(time.time() * 1000000000))
        room_split = room["id"].split(":")
        retention = room_split[1]  # nome Home
        measurement = room_split[2]
        humidity = random.randint(0, 100)
        temperature = random.randint(-10, 40)
        influx_point = build_influx_point(measurement, temperature, humidity, current_time)
        write_data(room["usernameID"], retention, influx_point, influx_url)


def write_data(database, retention, influx_point, influx_url):
    influx_write_url = f"{influx_url}/write?db={database}&rp={retention}"
    response = requests.post(influx_write_url, data=influx_point)
    if response.status_code != 204:
        print(f"Failed to write data to InfluxDB: {response.content}")


def build_influx_point(measurement, temperature, humidity, current_time):
    return f"{measurement} temperature={temperature},humidity={humidity} {current_time}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process data from API and send to InfluxDB.')
    parser.add_argument('be_url', type=str)
    parser.add_argument("-i", '--influx_url', type=str, help='URL of the InfluxDB endpoint', required=True)
    args = vars(parser.parse_args())

    process_data_be(args['be_url'], args['influx_url'])
