import subprocess
import time
import re
from datetime import datetime, timezone

import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


token = os.environ.get("INFLUXDB_TOKEN")
org = "ESLAB"
url = "http://localhost:8086"
bucket = "ptp_metrics"

# Initialize the database client
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

interface = "enx381428f4865c"


def collect_ptp_data():
    # Simulate sending PMC command and receiving output
    response = subprocess.run(
        ["sudo", "pmc", "-2", "-i", interface, "GET CURRENT_DATA_SET"],
        capture_output=True,
        text=True,
    )
    data = parse_response(response.stdout)
    # print(data)
    offsets = [datum["offset_from_master"] for datum in data]
    precision = max(offsets) - min(offsets)
    store_data(data, precision)


def parse_response(response):
    # Placeholder for response parsing logic
    # Initialize data storage
    data_list = []

    # Split the response into lines for easier processing
    lines = response.strip().split("\n")

    # Temporary storage for parsing data
    temp_data = {}

    # Regular expressions to match and capture key data
    port_identity_pattern = re.compile(
        r"^\s*([0-9a-f]{6}\.[0-9a-f]{4}\.[0-9a-f]{6}-\d+)"
    )
    offset_pattern = re.compile(r"offsetFromMaster\s+([-]?\d+\.?\d*)")
    path_delay_pattern = re.compile(r"meanPathDelay\s+(\d+\.?\d*)")

    # Iterate through each line of the response
    for line in lines:
        # Check for port identity
        port_match = port_identity_pattern.match(line)
        if port_match:
            # If starting new device block, save previous and start new
            if temp_data:
                data_list.append(temp_data)
                temp_data = {}
            temp_data["device_id"] = port_match.group(1)

        # Check for offset from master
        offset_match = offset_pattern.search(line)
        if offset_match:
            temp_data["offset_from_master"] = float(offset_match.group(1))

        # Check for mean path delay
        path_delay_match = path_delay_pattern.search(line)
        if path_delay_match:
            temp_data["mean_path_delay"] = float(path_delay_match.group(1))

    # Append the last parsed block if any
    if temp_data:
        data_list.append(temp_data)

    # Map data list to the desired return format
    parsed_data = []
    for device_data in data_list:
        parsed_data.append(
            {
                "time": int(time.time() * 1e9),  # Timestamp of the parsing event
                "device_id": device_data.get(
                    "device_id", "unknown"
                ),  # Default if not found
                "offset_from_master": device_data.get(
                    "offset_from_master", 0
                ),  # Default if not found
                "mean_path_delay": device_data.get(
                    "mean_path_delay", 0
                ),  # Default if not found
            }
        )

    return parsed_data


def store_data(data, precision):
    for datum in data:
        point = (
            Point("ptp")
            .tag("device_id", datum["device_id"])
            .time(datum["time"], WritePrecision.NS)
            .field("offset_from_master", datum["offset_from_master"])
            .field("mean_path_delay", datum["mean_path_delay"])
            .field("precision", precision)
        )
        # print("Storing Point", point)
        write_api.write(bucket=bucket, org="ESLAB", record=point)


# Schedule this to run at regular intervals

if __name__ == "__main__":
    while True:
        collect_ptp_data()
        time.sleep(1)
