#-*- coding:utf-8 -*-

import sys

from watna_location import settings
from django.core.management import setup_environ
setup_environ(settings)

from location.models import Location

list_file = sys.argv[1]

for location in Location.objects.all():
    location.city = location.city.strip()
    location.city = location.city.replace(u'จ.','')
    location.city = location.city.replace(u'จังหวัด','')
    location.city = location.city.strip()
    location.city = location.city.split()[0]
    location.save()

with open(list_file) as f:
    for line in f:
        if line.strip() == '':
            continue
        src, dest = line.rstrip().split('|')
        print src, '->', dest
        print Location.objects.filter(country='TH', city=src).update(city=dest.strip())
