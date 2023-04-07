#!/usr/bin/env python3

# DSNY_Frequencies.csv comes from https://data.cityofnewyork.us/City-Government/DSNY-Frequencies/rv63-53db/

import csv, json, sys
csv.field_size_limit(sys.maxsize)

data = {
  "type": "FeatureCollection", 
  "crs": {
    "type": "name", 
    "properties": {
      "name": "urn: ogc:def:crs:OGC:1.3:CRS84"
    }
  }, 
  "features": []
}

with open('./DSNY_Frequencies.csv', 'r') as csvfile:
  for row in [dict(row) for row in csv.DictReader(csvfile)]:
    # round to 5 decimals, error is about 3ft -- https://en.wikipedia.org/wiki/Decimal_degrees
    # remove '"MULTIPOLYGON (((' clutter from source csv to be just coordinates
    tmp_a = [e.lstrip().split(' ') for e in row["multipolygon"].split('(')[3].split(')')[0].split(',')]
    # convert to floats to trim to 5 decimals, then stringify
    tmp_b = [json.dumps([float('%.5f'%float(y[0])), float('%.5f'%float(y[1]))]) for y in tmp_a ]
    # remove duplicates while preserving order,
    tmp_set = set()
    tmp_c = []
    for x in tmp_b:
      if x not in tmp_set:
        tmp_set.add(x)
        tmp_c.append(x)

    # convert json arrays back to lists of floats
    tmp_d = [json.loads(x) for x in tmp_c]  

    data['features'].append({
      "type": "Feature",
      "properties": {
        "bulk": row["FREQ_BULK"].split(", "), 
        "recycling": row["FREQ_RECYCLING"].split(", "), 
        "refuse": row["FREQ_REFUSE"].split(", "), 
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [tmp_d]
      }
    })

with open('data.json', 'w') as f:
    json.dump(data, f)
