#!/usr/bin/env python3
import sys

current_region = None
previous_data = None
previous_month = None

for line in sys.stdin:
    line = line.strip()
    key, value = line.split("\t")
    
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
            print(f"{current_region}\t{month}\t{increase:.2f}")

    previous_data = data
    previous_month = month