import csv
import datetime
import json
import sys
from pathlib import Path

base_dir = sys.argv[1]

writer = csv.DictWriter(
    sys.stdout, fieldnames=["timestamp", "outages", "affected customers"]
)
writer.writeheader()

for filename in sorted(Path(base_dir).glob("dte_*.json")):
    row = {}
    timestamp_string = str(filename).split("_")[1].split(".")[0]
    row["timestamp"] = (
        datetime.datetime.strptime(timestamp_string, "%Y%m%d%H%M%S")
        .replace(tzinfo=datetime.timezone.utc)
        .isoformat()
    )

    with open(filename) as outage_file:
        outages = json.load(outage_file)

    row["outages"] = sum(outage["desc"]["n_out"] for outage in outages)
    row["affected customers"] = sum(
        outage["desc"]["cust_a"]["val"] for outage in outages
    )
    writer.writerow(row)
