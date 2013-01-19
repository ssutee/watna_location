from django.core.management import setup_environ
import watna_location.settings
setup_environ(watna_location.settings)

from location.models import Province, Region

import sys

with open(sys.argv[1]) as fp:
    region_name = ''
    for line in fp:
        if line[0] == ' ':            
            province = Province.objects.filter(name=line.strip())[0]
            province.region = region
            province.save()
        else:
            region_name = line.strip()
            region = Region.objects.filter(name=region_name)[0]