#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    fields = line.split(",")

    if len(fields) < 8:
        continue

    try:
        region = fields[0]  # 광역 단체명
        month = int(fields[4])  # 개최기간(월)
        festival_type = fields[3]  # 축제 유형
        data = float(fields[7])  # 누적 코로나 감염자 수
    except ValueError:
        continue

    print(f"{region}_{month}\t{festival_type}\t{data}")
