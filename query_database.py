import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


token = os.environ.get("INFLUXDB_TOKEN")
org = "ESLAB"
url = "http://localhost:8086"
bucket = "ptp_metrics"

# Initialize the database client
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

query_api = client.query_api()

query = """from(bucket: "ptp_metrics")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "ptp")"""
tables = query_api.query(query, org="ESLAB")

print(tables)
for table in tables:
    for record in table.records:
        print(record)
