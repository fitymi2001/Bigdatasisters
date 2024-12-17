#!/usr/bin/env python3
import sys

current_region = None
previous_data = None
previous_month = None

festival_type_data = {}

for line in sys.stdin:
    line = line.strip()
    parts = line.split("\t")
    if len(parts) != 3:
        continue

    key, festival_type, value = parts
    try:
        data = float(value)
    except ValueError:
        continue

    region, month = key.split("_")
    month = int(month)

    if current_region != region:
        current_region = region
        previous_data = None
        previous_month = None

    if previous_data is not None and previous_month is not None:
        if month == previous_month + 1:
            increase = data - previous_data
            if festival_type not in festival_type_data:
                festival_type_data[festival_type] = {"total_increase": 0.0, "count": 0}
            festival_type_data[festival_type]["total_increase"] += increase
            festival_type_data[festival_type]["count"] += 1

    previous_data = data
    previous_month = month

for festival_type, stats in festival_type_data.items():
    avg_increase = stats["total_increase"] / stats["count"] if stats["count"] > 0 else 0.0
    print(f"{festival_type}\t{avg_increase:.2f}")
