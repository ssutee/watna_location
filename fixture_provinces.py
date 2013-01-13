#!/usr/bin/env python

import sys, json

provinces = []
pk = 1
with open(sys.argv[1]) as f:
    for line in f:
        province = {}
        province['pk'] = pk
        province['model'] = 'location.province'
        province['fields'] = {'name': line.strip()}
        provinces.append(province)
        pk += 1
        
print json.dumps(provinces)
