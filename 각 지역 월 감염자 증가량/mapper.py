#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    fields = line.split(",")

    if len(fields) < 8:
        continue

    try:
        지역 = fields[0]  # 광역 단체명
        월 = int(fields[4])
        data = float(fields[7])
    except ValueError:
        continue

    print(f"{지역}_{월}\t{data}")
